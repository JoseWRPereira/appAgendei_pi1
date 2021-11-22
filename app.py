from flask import Flask
from flask import redirect, url_for, render_template, request
from datetime import date, timedelta, datetime
import psycopg2
import psycopg2.extras
from psycopg2 import Error



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
        self.host = 'ec2-35-168-80-116.compute-1.amazonaws.com'
        self.database = 'db11rl4t5fok51'
        self.user = 'mkquynsqfbowgn'
        self.port = '5432'
        self.password = '9ab6e907db802c1d080322a55145014df75063d39e3aa405a244a6a7cf4e1524'
        self.uri = 'postgres://mkquynsqfbowgn:9ab6e907db802c1d080322a55145014df75063d39e3aa405a244a6a7cf4e1524@ec2-35-168-80-116.compute-1.amazonaws.com:5432/db11rl4t5fok51'
        self.heroku_cli = 'heroku pg:psql postgresql-reticulated-70968 --app agendei-pi1'


dbcredential = DBCredential_online()

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



class Calendario:
    def __init__(self):
        self.data = date.today()
        self.delta = 0
    def get_data(self):
        return(self.data + timedelta(days = self.delta))
    def inc_delta(self):
        self.delta = self.delta + 1
    def dec_delta(self):
        self.delta = self.delta - 1

class Login:
    def __init__(self):
        self.nome = "Admin"
        self.nif = 1
        self.senha = "admin"




###############################################################################
################################################################ Instanciamento
###############################################################################
app = Flask(__name__)
calendario = Calendario()
login = Login()



###############################################################################
######################################################################### index
###############################################################################

@app.route("/")
def index():
    return render_template('index.html', userName=login.nome )






###############################################################################
########################################################################## main
###############################################################################

@app.route("/main")
def main():
    data = str(calendario.get_data())
    reservas = sql_fetch("SELECT id,carrinho,usuario_manha,usuario_tarde,usuario_noite FROM reserva WHERE data='{}' ORDER BY carrinho DESC;".format(data) )
    return render_template('main.html', userName=login.nome, data=data, reservas=reservas )

@app.route("/main/datadec", methods=['GET','POST'])
def maindatadec():
    calendario.dec_delta()
    return redirect(url_for('main'))

@app.route("/main/datainc", methods=['GET','POST'])
def maindatainc():
    calendario.inc_delta()
    return redirect(url_for('main'))





###############################################################################
######################################################################### login
###############################################################################
@app.route("/login", methods=['GET','POST'])
def logon():
    if request.method == 'POST':
        usuario         = Usuario()
        usuario.nome    = str( request.form['user'])
        usuario.senha   = str( request.form['pwd'])
        user = sql_fetch("SELECT id,nif,nome,senha FROM usuario WHERE nome='{}';".format(usuario.nome))
        if user[0][3]==usuario.senha:
            login.nome = user[0][2]
            login.nif = user[0][1]
            return redirect(url_for('index'))
        else:
            login.nome = ""
            login.nif = ""
            return redirect(url_for('loginerror'))
    else:
        usuarios = sql_fetch("SELECT id,nif,nome FROM usuario;")
        return render_template('login.html', userName=login.nome, usuarios=usuarios)

@app.route("/loginerror")
def loginerror():
    return render_template('login_error.html')

@app.route("/logoff")
def logoff():
    login.nif = 0
    login.nome = ''
    login.senha = ''
    return redirect(url_for('index'))


###############################################################################
####################################################################### agendar
###############################################################################
@app.route("/agendar")
def agendar():
    data = str(calendario.get_data())
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
    return render_template('agendar.html', userName=login.nome, data=data, carrinhos=carrinhos, listas=listas )

@app.route("/agendar/datadec", methods=['GET','POST'])
def agendardatadec():
    calendario.dec_delta()
    return redirect(url_for('agendar'))

@app.route("/agendar/datainc", methods=['GET','POST'])
def agendardatainc():
    calendario.inc_delta()
    return redirect(url_for('agendar'))

@app.route("/agendar/carrinho/<id>/<car>/<periodo>/<cmd>", methods=['GET','POST'])
def agendarcarrinho(id, car, periodo, cmd):
    data = str(calendario.get_data())

    if 'INSERT' in cmd:
        if 'm' in periodo:
            sql_cmd("INSERT INTO reserva (data, carrinho, usuario_manha) VALUES ('{}','{}','{}');".format(data, car, login.nome ) )
        elif 'v' in periodo:
            sql_cmd("INSERT INTO reserva (data, carrinho, usuario_tarde) VALUES ('{}','{}','{}');".format(data, car, login.nome ) )
        elif 'n' in periodo:
            sql_cmd("INSERT INTO reserva (data, carrinho, usuario_noite) VALUES ('{}','{}','{}');".format(data, car, login.nome ) )
    elif 'UPDATE' in cmd:
        if 'm' in periodo:
            sql_cmd("UPDATE reserva SET usuario_manha='{}' WHERE id='{}';".format( login.nome, id ) )
        elif 'v' in periodo:
            sql_cmd("UPDATE reserva SET usuario_tarde='{}' WHERE id='{}';".format( login.nome, id ) )
        elif 'n' in periodo:
            sql_cmd("UPDATE reserva SET usuario_noite='{}' WHERE id='{}';".format( login.nome, id ) )

    return redirect(url_for('agendar'))



###############################################################################
####################################################################### excluir
###############################################################################
@app.route("/excluir")
def excluir():
    reservas = sql_fetch("SELECT id,data,carrinho,usuario_manha,usuario_tarde,usuario_noite FROM reserva WHERE usuario_manha='{}' OR usuario_tarde='{}' OR usuario_noite='{}' AND data>='{}' ORDER BY data DESC;".format( login.nome, login.nome, login.nome, calendario.data ) )
    
    return render_template('excluir.html', userName=login.nome, reservas=reservas )

@app.route("/excluir/<id>")
def excluir_id(id):
    users = sql_fetch("SELECT usuario_manha, usuario_tarde, usuario_noite FROM reserva WHERE id='{}';".format(id))
    # return "{} {} {} : {} : {} {} {}".format(users[0][0], users[0][1], users[0][2], login.nome, login.nome == users[0][0], login.nome == users[0][1], login.nome == users[0][2])
    if login.nome == users[0][0]:
        sql_cmd("UPDATE reserva SET usuario_manha=NULL WHERE id='{}';".format(id) )
    if login.nome == users[0][1]:
        sql_cmd("UPDATE reserva SET usuario_tarde=NULL WHERE id='{}';".format(id) )
    if login.nome == users[0][2]:
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
        return render_template('gerenciar_usuarios.html', userName=login.nome, usuarios=usuarios )


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
        return render_template('gerenciar_carrinhos.html', userName=login.nome, carrinhos=carrinhos )


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
        reserva = Reserva()
        reserva.data = request.form['calendario']
        reserva.periodo = str(request.form['periodo'])
        reserva.carrinho = str(request.form['car'])
        if reserva.periodo == 'M':
            reserva.usuario_manha = request.form['usuario']
            sql_cmd("INSERT INTO reserva (data, carrinho, usuario_manha) VALUES ('{}','{}','{}');".format(reserva.data, reserva.carrinho, reserva.usuario_manha ) )
        elif reserva.periodo == 'V':
            reserva.usuario_tarde = request.form['usuario']
            sql_cmd("INSERT INTO reserva (data, carrinho, usuario_tarde) VALUES ('{}','{}','{}');".format(reserva.data, reserva.carrinho, reserva.usuario_tarde ) )
        else:
            reserva.usuario_noite = request.form['usuario']
            sql_cmd("INSERT INTO reserva (data, carrinho, usuario_noite) VALUES ('{}','{}','{}');".format(reserva.data, reserva.carrinho, reserva.usuario_noite ) )
        return redirect(url_for('gerenciarreservas'))
    else:
        carrinhos = sql_fetch("SELECT id,nome FROM carrinho;")
        usuarios = sql_fetch("SELECT nif,nome FROM usuario;")
        reservas = sql_fetch("SELECT * FROM reserva ORDER BY id DESC;")
        return render_template('gerenciar_reservas.html', userName=login.nome, carrinhos=carrinhos, usuarios=usuarios, reservas=reservas)


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
    app.run(host="0.0.0.0", port=5000, debug=True)

###############################################################################
###############################################################################
