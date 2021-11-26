from flask import Flask
from flask import redirect, url_for, render_template, request
from flask import session, flash
from datetime import date, timedelta
import psycopg2
import psycopg2.extras
from psycopg2 import Error



#### VER
# Sesseions
# https://www.youtube.com/watch?v=ddjT_Gdp_cc
# https://www.youtube.com/watch?v=iIhAfX4iek0


###############################################################################
##################################### Conexão com o Banco de Dados - PostgreSQL
###############################################################################

class DBCredential_local:
    def __init__(self):
        self.host = '127.0.0.1'
        self.database = 'pi1db'
        self.user = 'postgres'
        self.port = '5432'
        self.password = 'postgres'
        self.uri = "postgresql://postgres:postgres@localhost:5432/pi1db"

class DBCredential_online:
    def __init__(self):
        self.host = 'ec2-52-20-143-167.compute-1.amazonaws.com'
        self.database = 'd1f1r9u6nff5vk'
        self.user = 'kgjlgrirpawegc'
        self.port = '5432'
        self.password = 'b6e2ce9c166a323946076f92d4cf13911b342f777555a391e7cc599208f83b39'
        self.uri = 'postgres://kgjlgrirpawegc:b6e2ce9c166a323946076f92d4cf13911b342f777555a391e7cc599208f83b39@ec2-52-20-143-167.compute-1.amazonaws.com:5432/d1f1r9u6nff5vk'
        self.heroku_cli = 'heroku pg:psql postgresql-octagonal-47192 --app agendei-pi1'


dbcredential = DBCredential_local()

def sql_fetch(sql):
    try:
        connection = psycopg2.connect( dbcredential.uri )
        cursor = connection.cursor()
        cursor.execute(sql)
        print("SQL FETCH: ", sql, "\n")
        lista = cursor.fetchall()
        for l in lista:
            print("  ", l, "\n")
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL: ", error)
        cursor.execute("ROLLBACK;")
        lista = []
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
            return lista



def sql_cmd(sql):
    try:
        connection = psycopg2.connect(  database=dbcredential.database,
                                        user=dbcredential.user,
                                        password=dbcredential.password,
                                        host=dbcredential.host,
                                        port=dbcredential.port
                                    )
        cursor = connection.cursor()
        cursor.execute(sql)
        print("SQL CMD: ", sql, "\n")
        cursor.execute("COMMIT;")
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL: ", error)
        cursor.execute("ROLLBACK;")
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")





###############################################################################
####################################################################### Classes
###############################################################################

class Usuario:
    def __init__(self):
        self.id = 0
        self.nif = ""
        self.nome = ""
        self.senha = ""

class Carrinho:
    def _init__(self):
        self.id = 0
        self.nome = ""

class Reserva:
    def __init__(self):
        self.data = date.today()
        self.carrinho = ""
        self.usuario_manha = ""
        self.usuario_tarde = ""
        self.usuario_noite = ""
        self.periodo = ''








###############################################################################
################################################################ Instanciamento
###############################################################################
app = Flask(__name__)
app.secret_key = "agendei_pi1"



###############################################################################
######################################################################### login
###############################################################################
@app.route("/login", methods=['GET','POST'])
def logon():
    if request.method == 'POST':
        nome    = str( request.form['user'])
        senha   = str( request.form['pwd'])
        user = sql_fetch("SELECT id,nif,nome,senha FROM usuario WHERE nome='{}';".format(nome))
        if user and user[0][3]==senha:
            session['username'] = request.form['user']
            session['nif'] = user[0][1]
            return redirect(url_for('index'))
        else:
            session['username'] = None
            session['nif'] = None
            return redirect(url_for('loginerror'))
    else:
        usuarios = sql_fetch("SELECT id,nif,nome FROM usuario;")
        return render_template('login.html', usuarios=usuarios)

@app.route("/loginerror")
def loginerror():
    return render_template('login_error.html')

@app.route("/logoff")
def logoff():
    session.pop('username', None)
    session.pop('data', None )
    session.pop('delta', None)
    return redirect(url_for('index'))




###############################################################################
######################################################################### data
###############################################################################
def get_data():
    return(date.today() + timedelta(days = session['delta']))
def inc_delta():
    session['delta'] = session['delta'] + 1
def dec_delta():
    session['delta'] = session['delta'] - 1

###############################################################################
######################################################################### index
###############################################################################

@app.route("/")
def index():
    session['data'] = date.today()
    session['delta'] = 0
    return render_template('index.html')






###############################################################################
########################################################################## main
###############################################################################

@app.route("/main/")
def main():
    reservas = sql_fetch("SELECT id,carrinho,usuario_manha,usuario_tarde,usuario_noite FROM reserva WHERE data='{}' ORDER BY carrinho DESC;".format(get_data()) )
    return render_template('main.html', data=get_data(), reservas=reservas )

@app.route("/main/datadec", methods=['GET','POST'])
def maindatadec():
    dec_delta()
    return redirect(url_for('main'))

@app.route("/main/datainc", methods=['GET','POST'])
def maindatainc():
    inc_delta()
    return redirect(url_for('main'))





###############################################################################
####################################################################### agendar
###############################################################################
@app.route("/agendar/")
def agendar():
    if session['delta'] < 0:
        session['delta'] = 0
    data = str(get_data())
    carrinhos = sql_fetch("SELECT id,nome FROM carrinho;")
    listas = []
    for car in carrinhos:
        lista = []
        res = sql_fetch("SELECT usuario_manha, usuario_tarde, usuario_noite, id FROM reserva WHERE data='{}' AND carrinho='{}';".format(data, car[0]))
        try:
            m = res[0][0] if res[0][0]!=None else '@'
            v = res[0][1] if res[0][1]!=None else '@'
            n = res[0][2] if res[0][2]!=None else '@'
            rid = res[0][3]
            cmd = 'UPDATE'
        except:
            m = '@'
            v = '@'
            n = '@'
            rid = None
            cmd = 'INSERT'
        lista.insert(0, rid )
        lista.insert(1, car[0] )
        lista.insert(2, m )
        lista.insert(3, v )
        lista.insert(4, n )
        lista.insert(5, cmd)
        listas.append(lista)
    return render_template('agendar.html', data=data, carrinhos=carrinhos, listas=listas )

@app.route("/agendar/datadec", methods=['GET','POST'])
def agendardatadec():
    if session['delta'] < 0:
        session['delta'] = 0
    else:
        dec_delta()
    return redirect(url_for('agendar'))

@app.route("/agendar/datainc", methods=['GET','POST'])
def agendardatainc():
    inc_delta()
    return redirect(url_for('agendar'))

@app.route("/agendar/carrinho/<id>/<car>/<periodo>/<cmd>", methods=['GET','POST'])
def agendarcarrinho(id, car, periodo, cmd):
    data = str(get_data())

    if 'INSERT' in cmd:
        if 'm' in periodo:
            sql_cmd("INSERT INTO reserva (data, carrinho, usuario_manha) VALUES ('{}','{}','{}');".format(data, car, session['username'] ) )
        elif 'v' in periodo:
            sql_cmd("INSERT INTO reserva (data, carrinho, usuario_tarde) VALUES ('{}','{}','{}');".format(data, car, session['username'] ) )
        elif 'n' in periodo:
            sql_cmd("INSERT INTO reserva (data, carrinho, usuario_noite) VALUES ('{}','{}','{}');".format(data, car, session['username'] ) )
    elif 'UPDATE' in cmd:
        if 'm' in periodo:
            sql_cmd("UPDATE reserva SET usuario_manha='{}' WHERE id='{}';".format( session['username'], id ) )
        elif 'v' in periodo:
            sql_cmd("UPDATE reserva SET usuario_tarde='{}' WHERE id='{}';".format( session['username'], id ) )
        elif 'n' in periodo:
            sql_cmd("UPDATE reserva SET usuario_noite='{}' WHERE id='{}';".format( session['username'], id ) )

    return redirect(url_for('agendar'))



###############################################################################
####################################################################### excluir
###############################################################################
@app.route("/excluir")
def excluir():
    reservas = sql_fetch("SELECT id,data,carrinho,usuario_manha,usuario_tarde,usuario_noite FROM reserva WHERE (usuario_manha='{}' OR usuario_tarde='{}' OR usuario_noite='{}') AND data>='{}' ORDER BY data DESC;".format( session['username'], session['username'], session['username'], date.today() ) )
    return render_template('excluir.html', reservas=reservas )

@app.route("/excluir/<id>")
def excluir_id(id):
    users = sql_fetch("SELECT usuario_manha, usuario_tarde, usuario_noite FROM reserva WHERE id='{}';".format(id))
    if session['username'] == users[0][0]:
        sql_cmd("UPDATE reserva SET usuario_manha=NULL WHERE id='{}';".format(id) )
    if session['username'] == users[0][1]:
        sql_cmd("UPDATE reserva SET usuario_tarde=NULL WHERE id='{}';".format(id) )
    if session['username'] == users[0][2]:
        sql_cmd("UPDATE reserva SET usuario_noite=NULL WHERE id='{}';".format(id) )
    return redirect(url_for('excluir'))


###############################################################################
##################################################################### Gerenciar
###############################################################################

###############################################################################
############################################################ Gerenciar usuarios
################################# (nif), nome, [disciplina]->disciplina(codigo)
###############################################################################

@app.route("/gerenciar/usuarios", methods=['GET','POST'])
def gerenciarusuarios():
    if request.method == 'POST':
        usuario         = Usuario()
        usuario.nif     = str( request.form['nif'])
        usuario.nome    = str( request.form['nome'])
        usuario.senha   = str( request.form['senha'])
        sql_cmd("INSERT INTO usuario (nif, nome, senha) VALUES ('{}','{}','{}');".format(usuario.nif, usuario.nome, usuario.senha ) )
        return redirect(url_for('gerenciarusuarios'))
    else:
        usuarios = sql_fetch("SELECT id,nif,nome FROM usuario;")
        return render_template('gerenciar_usuarios.html', usuarios=usuarios )


@app.route("/gerenciar/usuarios/del/<id>")
def gerenciarusuariosdel(id):
    sql_cmd("DELETE FROM usuario WHERE id='{}';".format(id) )
    return redirect(url_for('gerenciarusuarios'))





###############################################################################
########################################################### Gerenciar carrinhos
################################################## (id), nome, qtd_equipamentos
###############################################################################
@app.route("/gerenciar/carrinhos", methods=['GET','POST'])
def gerenciarcarrinhos():
    if request.method == 'POST':
        carrinho = Carrinho()
        carrinho.nome = str( request.form['nome'] )
        sql_cmd( "INSERT INTO carrinho (nome) VALUES ('{}');".format(carrinho.nome) )
        return redirect(url_for('gerenciarcarrinhos'))
    else:
        carrinhos = sql_fetch("SELECT id,nome FROM carrinho;")
        return render_template('gerenciar_carrinhos.html', carrinhos=carrinhos )


@app.route("/gerenciar/carrinhos/del/<id>")
def gerenciarcarrinhosdel(id):
    sql_cmd("DELETE FROM carrinho WHERE id='{}';".format(id) )
    return redirect(url_for('gerenciarcarrinhos'))





###############################################################################
############################################################ Gerenciar reservas
###### id, data, carrinho, userM, userV, userN
###############################################################################
@app.route("/gerenciar/reservas", methods=['GET','POST'])
def gerenciarreservas():
    if request.method == 'POST':
        # reserva = Reserva()
        data = request.form['calendario']
        periodo = str(request.form['periodo'])
        carrinho = str(request.form['car'])
        if periodo == 'M':
            usuario_manha = str(request.form['user'])
            sql_cmd("INSERT INTO reserva (data, carrinho, usuario_manha) VALUES ('{}','{}','{}');".format(data, carrinho, usuario_manha ) )
        elif periodo == 'V':
            usuario_tarde = str(request.form['user'])
            sql_cmd("INSERT INTO reserva (data, carrinho, usuario_tarde) VALUES ('{}','{}','{}');".format(data, carrinho, usuario_tarde ) )
        else:
            usuario_noite = str(request.form['user'])
            sql_cmd("INSERT INTO reserva (data, carrinho, usuario_noite) VALUES ('{}','{}','{}');".format(data, carrinho, usuario_noite ) )
        return redirect(url_for('gerenciarreservas'))
    else:
        carrinhos = sql_fetch("SELECT id,nome FROM carrinho;")
        usuarios = sql_fetch("SELECT nif,nome FROM usuario;")
        reservas = sql_fetch("SELECT * FROM reserva ORDER BY id DESC;")
        return render_template('gerenciar_reservas.html', carrinhos=carrinhos, usuarios=usuarios, reservas=reservas)


@app.route("/gerenciar/reservas/del/<id>")
def gerenciarreservasdel(id):
    sql_cmd("DELETE FROM reserva WHERE id='{}';".format(id))
    return redirect(url_for('gerenciarreservas'))



###############################################################################
################################################################# create tables
###############################################################################

@app.route("/resetdb")
def resetdb():
    sql_cmd("DROP TABLE IF EXISTS reserva;")
    sql_cmd("DROP TABLE IF EXISTS carrinho;")
    sql_cmd("DROP TABLE IF EXISTS usuario;")
    sql_cmd("CREATE TABLE IF NOT EXISTS usuario  ( id SERIAL PRIMARY KEY, nif INTEGER, nome TEXT, senha TEXT );")
    sql_cmd("CREATE TABLE IF NOT EXISTS carrinho ( id SERIAL PRIMARY KEY, nome TEXT );")
    sql_cmd("CREATE TABLE IF NOT EXISTS reserva  ( id SERIAL PRIMARY KEY, data DATE, carrinho TEXT, usuario_manha TEXT, usuario_tarde TEXT, usuario_noite TEXT );")
    sql_cmd("INSERT INTO usuario ( nif, nome, senha) VALUES ('{}','{}','{}');".format( 1,"Admin", "admin" ) )
    return redirect(url_for('index'))




###############################################################################
###############################################################################

if __name__ == '__main__':
    app.run()

###############################################################################
###############################################################################
