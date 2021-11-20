from flask import Flask
from flask import redirect, url_for, render_template, request
import os
from datetime import date, timedelta, datetime
from werkzeug.exceptions import abort
import psycopg2
import psycopg2.extras
from psycopg2 import Error



###############################################################################
##################################### Conexão com o Banco de Dados - PostgreSQL
###############################################################################
def sql_fetch(sql):
    try:
        cmd = "postgresql://postgres:postgres@localhost:5432/pi1db"
        connection = psycopg2.connect( cmd )
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
        connection = psycopg2.connect(  database="pi1db",
                                        user="postgres",
                                        password="postgres",
                                        host="127.0.0.1",
                                        port="5432"
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
        
# class Usuario:
#     def __init__(self):
#         self.nif = 0
#         self.nome = ""
#         self.senha = ""
#     def set_nif(self, nif):
#         self.nif = nif
#     def set_nome(self,nome):
#         self.nome = nome
#     def set_disciplina(self,disciplina):
#         self.disciplina = disciplina
#     def set_senha(self,senha):
#         self.senha = senha
#     def get_nif(self):
#         return(self.nif)
#     def get_nome(self):
#         return(self.nome)
#     def get_disciplina(self):
#         return(self.disciplina)
#     def get_senha(self):
#         return(self.senha)


class Carrinho:
    def _init__(self):
        self.id = 0
        self.nome = ""

# class Carrinho:
#     def _init__(self):
#         self.id=0
#         self.nome = ""
#         self.qtd_equipamentos = 0
#     def set_id(self, id):
#         self.id = id
#     def set_nome(self, nome):
#         self.nome = nome
#     def set_qtd_equipamentos(self, qtd):
#         self.qtd_equipamentos = qtd
#     def get_id(self):
#         return(self.id)
#     def get_nome(self):
#         return(self.nome)
#     def get_qtd_equipamentos(self):
#         return(self.qtd_equipamentos)
        

# class Reserva:#( id, data, periodo, carrinho_id, usuario_id
#     def __init__(self):
#         self.data = 0
#         self.periodo = 0
#         self.carrinho_id = 0
#         self.usuario_id = 0
#     def set_data(self,data):
#         self.data = data
#     def set_periodo(self,periodo):
#         self.periodo = periodo
#     def set_carrinho_id(self,carrinho):
#         self.carrinho_id = carrinho
#     def set_usuario_id(self,usuario):
#         self.usuario_id = usuario
#     def get_data(self):
#         return(self.data)
#     def get_periodo(self):
#         return(self.periodo)
#     def get_carrinho_id(self):
#         return(self.carrinho_id)
#     def get_usuario_id(self):
#         return(self.usuario_id)
    

class Calendario:
    def __init__(self):
        self.data = date.today()
        self.delta = 0
    def set_delta(self, delta):
        self.delta = delta
    def get_delta(self):
        return(self.delta)
    def get_data(self):
        return(self.data + timedelta(days = self.delta))
    def get_data_today(self):
        return( date.today() )

class Login:
    def __init__(self):
        self.nome = "Admin"
        self.nif = 1
        self.senha = "admin"
    # def get_usuario(self):
    #     return(self.usuario)
    # def set_usuario(self,user):
    #     self.usuario = user
    # def get_nif(self):
    #     return(self.nif)
    # def set_nif(self,nif):
    #     self.nif = nif
    # def get_pwd(self):
    #     return(self.pwd)
    # def set_pwd(self,pwd):
    #     self.pwd = pwd




###############################################################################
################################################################ Instanciamento
###############################################################################
app = Flask(__name__)

# usuario = Usuario()
# carrinho = Carrinho()
# reserva = Reserva()
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
    # data1 = calendario.get_data()
    # sql = "SELECT id,data,periodo,carrinho_id,usuario_id FROM reserva WHERE data='{}';".format(data1)
    # lista1 = db_cmd(sql)

    # calendario.set_delta( calendario.get_delta()+1 )
    # data2 = calendario.get_data()
    # sql = "SELECT id,data,periodo,carrinho_id,usuario_id FROM reserva WHERE data='{}';".format(data2)
    # lista2 = db_cmd(sql)

    # calendario.set_delta( calendario.get_delta()+1 )
    # data3 = calendario.get_data()
    # sql = "SELECT id,data,periodo,carrinho_id,usuario_id FROM reserva WHERE data='{}';".format(data3)
    # lista3 = db_cmd(sql)

    # calendario.set_delta( calendario.get_delta()-2 )
    # data = calendario.get_data()
    # return render_template('main.html', userName=acesso.get_usuario(), lista1=lista1, data1=data1, lista2=lista2, data2=data2, lista3=lista3, data3=data3, data=data )
    return render_template('main.html', userName=login.nome )

@app.route("/main/datadec", methods=['GET','POST'])
def maindatadec():
    calendario.set_delta( calendario.get_delta()-1 )
    return redirect(url_for('main'))

@app.route("/main/datainc", methods=['GET','POST'])
def maindatainc():
    calendario.set_delta( calendario.get_delta()+1 )
    return redirect(url_for('main'))





###############################################################################
######################################################################### login
###############################################################################
# @app.route("/login")
# def login():
#     sql = "SELECT nif,nome FROM usuario;"
#     user = db_cmd(sql)
#     return render_template('login.html', user=user, userName=acesso.get_usuario() )

# @app.route("/login/validar", methods=['GET','POST'])
# def loginvalidar():
#     if request.method == 'POST':
#         acesso.set_usuario(request.form['browser'])
#         acesso.set_pwd(request.form['pwd'])
#         sql = "SELECT nif FROM usuario WHERE nome='{}';".format(acesso.get_usuario())
#         nif = db_cmd(sql)
#         acesso.set_nif( nif[0][0] )

#         sql = "SELECT senha FROM usuario WHERE nif='{}';".format(acesso.get_nif() )
#         senha = db_cmd(sql)
#         # return "{} == {}".format( senha[0][0], acesso.get_pwd() )
#         if senha[0][0] == acesso.get_pwd():
#             return redirect(url_for('agendar'))
#         else:
#             acesso.set_usuario("")
#             return redirect(url_for('loginerror'))

# @app.route("/loginerror")
# def loginerror():
#     return render_template('login_error.html')


# @app.route("/logoff")
# def logoff():
#     acesso.set_nif(0)
#     acesso.set_pwd("")
#     acesso.set_usuario("")
#     return redirect(url_for('index'))


###############################################################################
####################################################################### agendar
###############################################################################
# @app.route("/agendar")
# def agendar():
#     data = calendario.get_data()
#     sql = "SELECT id,nome FROM carrinho;"
#     listaCarrinhos = db_cmd(sql)
#     sql = "SELECT periodo,carrinho_id,usuario_id FROM reserva where data='{}' ORDER BY carrinho_id;".format(data)
#     listaReservas = db_cmd(sql)
#     listaPeriodos = (['M','Matutino'],['V','Vespertino'],['N','Noturno'])
#     lista = []
#     achei = 0
#     for p in listaPeriodos:
#         for c in listaCarrinhos:
#             achei = 0
#             for l in listaReservas:
#                 if p[0]==l[0] and c[0]==l[1]:
#                     achei = 1
#                     break
#             if not achei:
#                 dt = []
#                 # dt.append( datetime.now().strftime("%Y-%m-%d") )
#                 dt.append( data )
#                 lista.append( (dt,str(p[0]),str(c[0])) )
#     return render_template('agendar.html', lista=lista, userName=acesso.get_usuario() )


# @app.route("/agendar/datadec", methods=['GET','POST'])
# def agendardatadec():
#     calendario.set_delta( calendario.get_delta()-1 )
#     return redirect(url_for('agendar'))

# @app.route("/agendar/datainc", methods=['GET','POST'])
# def agendardatainc():
#     calendario.set_delta( calendario.get_delta()+1 )
#     return redirect(url_for('agendar'))

# @app.route("/agendar/carrinho/<id>/<periodo>", methods=['GET','POST'])
# def agendarcarrinho(id, periodo):
#     sql =  "INSERT INTO reserva (data, periodo, carrinho_id, usuario_id) VALUES ('{}','{}',{},'{}');".format(str(calendario.get_data()), str(periodo),int(id), int(acesso.get_nif()) )
#     db_cmd(sql)
#     return redirect(url_for('agendar'))



###############################################################################
####################################################################### excluir
###############################################################################
# @app.route("/excluir")
# def excluir():
#     sql = "SELECT id,data,periodo,carrinho_id FROM reserva WHERE usuario_id='{}' AND data>='{}';".format(acesso.get_nif(), calendario.get_data_today() )
#     lista = db_cmd(sql)
#     return render_template('excluir.html', lista=lista, userName=acesso.get_usuario() )

# @app.route("/excluir/<id>")
# def excluir_id(id):
#     sql = "DELETE FROM reserva WHERE id='{}';".format(id)
#     db_cmd(sql)
#     return redirect(url_for('excluir'))


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
###### (id), data, periodo, carrinho_id->carrinho(id), usuario_id->usuario(nif)
###############################################################################
# @app.route("/gerenciar/reservas", methods=['GET','POST'])
# def gerenciarreservas():
#     if request.method == 'POST':
#         reserva.set_data(request.form['calendario'])
#         reserva.set_periodo(request.form['periodo'])
#         reserva.set_carrinho_id(request.form['carrinho'])
#         reserva.set_usuario_id(request.form['usuario'])
#         return redirect(url_for('gerenciarreservasadd'))
#     else:
#         sql = "SELECT id,nome FROM carrinho;"
#         carrinho = db_cmd(sql)
#         sql = "SELECT nif,nome FROM usuario;"
#         usuario = db_cmd(sql)
#         sql = "SELECT * FROM reserva ORDER BY id DESC;"
#         lista = db_cmd(sql)
#         return render_template('gerenciar_reservas.html', lista=lista, carrinho=carrinho, usuario=usuario, userName=acesso.get_usuario())

# @app.route("/gerenciar/reservas/add")
# def gerenciarreservasadd():
#     sql =  "INSERT INTO reserva (data, periodo, carrinho_id, usuario_id) VALUES ('{}','{}','{}','{}');".format(str(reserva.get_data()), str(reserva.get_periodo()),str(reserva.get_carrinho_id()), str(reserva.get_usuario_id()) )
#     db_cmd(sql)
#     return redirect(url_for('gerenciarreservas'))

# @app.route("/gerenciar/reservas/del/<id>", methods=['GET', 'POST'])
# def gerenciarreservasdel(id):
#     sql = "DELETE FROM reserva WHERE id='{}';".format(id)
#     db_cmd(sql)
#     return redirect(url_for('gerenciarreservas'))



###############################################################################
################################################################# create tables
###############################################################################

@app.route("/resetdb")
def resetdb():
    sql_cmd("DROP TABLE IF EXISTS carrinho;")
    sql_cmd("DROP TABLE IF EXISTS usuario;")
    sql_cmd("CREATE TABLE IF NOT EXISTS usuario ( id SERIAL PRIMARY KEY, nif INTEGER, nome TEXT, senha TEXT );")
    sql_cmd("CREATE TABLE IF NOT EXISTS carrinho( id SERIAL PRIMARY KEY, nome TEXT );")
    sql_cmd("INSERT INTO usuario ( nif, nome, senha) VALUES ('{}','{}','{}');".format( 1,"Admin", "admin" ) )
    return redirect(url_for('index'))




###############################################################################
###############################################################################

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

###############################################################################
###############################################################################
