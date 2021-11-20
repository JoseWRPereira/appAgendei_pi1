from flask import Flask
from flask import redirect, url_for, render_template, request
import os
from datetime import date, timedelta, datetime
from werkzeug.exceptions import abort
import psycopg2
import psycopg2.extras
from psycopg2 import Error


# project_dir = os.path.dirname(os.path.abspath(__file__))
# database_file = "sqlite:///{}".format(os.path.join(project_dir,"database.db"))




###############################################################################
##################################### Conexão com o Banco de Dados - PostgreSQL
###############################################################################
def db_cmd(sql):
    select = sql.count('SELECT') + sql.count('select')
    lista = []
    try:
        # Connect to an existing database
        # cmd = "postgresql://postgres:postgres@localhost:5432/pi1db"
        # connection = psycopg2.connect( cmd )
        connection = psycopg2.connect(  database="pi1db",
                                        user="postgres",
                                        password="postgres",
                                        host="127.0.0.1",
                                        port="5432"
                                    )

        # Create a cursor to perform database operations
        cursor = connection.cursor()
        # # Print PostgreSQL details
        # print("PostgreSQL server information")
        # print(connection.get_dsn_parameters(), "\n")
        # # Executing a SQL query
        # cursor.execute("SELECT version();")
        # Fetch result
        # record = cursor.fetchone()
        # print("You are connected to - ", record, "\n")
        cursor.execute(sql)
        print("SQL: ", sql, "\n")
        if select > 0:
            lista = cursor.fetchall()
            print(" ", lista, "\n")
        cursor.execute("COMMIT;")
        # cursor.close()
        # connection.close()
        # print("PostgreSQL connection is closed")
        # if select > 0:
        #     return lista

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL: ", error)
        cursor.execute("ROLLBACK;")
        # cursor.close()
        # connection.close()
        lista = []
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
            if select > 0:
                return lista



# def db_cmd(sql):
#     select = sql.count('SELECT') + sql.count('select')
    # try:
    #     conn = mariadb.connect(
    #         host=db_conn_params["host"],
    #         port=db_conn_params["port"],
    #         user=db_conn_params["user"],
    #         password=db_conn_params["password"],
    #         database=db_conn_params["database"]
    #         )
    # except mariadb.Error as e:
    #     print(f"Error connection to MariaDB Platform: {e}")
    #     sys.exit(1)
    # cursor = conn.cursor()
    # cursor.execute(sql)
    # if select > 0:
    #     lista = cursor.fetchall()
    # conn.commit()
    # conn.close()
    # if select > 0:
    #     return lista




###############################################################################
####################################################################### Classes
###############################################################################
class Disciplina:
    def __init__(self):
        self.codigo = ""
        self.nome = ""
    def set_codigo(self, code):
        self.codigo = code
    def set_nome(self, name):
        self.nome = name
    def get_codigo(self):
        return(self.codigo)
    def get_nome(self):
        return(self.nome)

class Usuario:
    def __init__(self):
        self.nif = 0
        self.nome = "Visitante"
        self.disciplina = ""
        self.senha = ""
    def set_nif(self, nif):
        self.nif = nif
    def set_nome(self,nome):
        self.nome = nome
    def set_disciplina(self,disciplina):
        self.disciplina = disciplina
    def set_senha(self,senha):
        self.senha = senha
    def get_nif(self):
        return(self.nif)
    def get_nome(self):
        return(self.nome)
    def get_disciplina(self):
        return(self.disciplina)
    def get_senha(self):
        return(self.senha)

class Carrinho:
    def _init__(self):
        self.id=0
        self.nome = ""
        self.qtd_equipamentos = 0
    def set_id(self, id):
        self.id = id
    def set_nome(self, nome):
        self.nome = nome
    def set_qtd_equipamentos(self, qtd):
        self.qtd_equipamentos = qtd
    def get_id(self):
        return(self.id)
    def get_nome(self):
        return(self.nome)
    def get_qtd_equipamentos(self):
        return(self.qtd_equipamentos)
        
class Equipamento:# np, nome, carrinho, descricao, adquirido_em, status
    def __init__(self):
        self.np = 0
        self.nome = ""
        self.carrinho = 0
        self.descricao = ""
        self.adquisido_em = 0
        self.status = ""
    def set_np(self,np):
        self.np = np
    def set_nome(self,nome):
        self.nome = nome
    def set_carrinho(self,carrinho):
        self.carrinho = carrinho
    def get_np(self):
        return(self.np)
    def get_nome(self):
        return(self.nome)
    def get_carrinho(self):
        return(self.carrinho)


class Reserva:#( id, data, periodo, carrinho_id, usuario_id
    def __init__(self):
        self.data = 0
        self.periodo = 0
        self.carrinho_id = 0
        self.usuario_id = 0
    def set_data(self,data):
        self.data = data
    def set_periodo(self,periodo):
        self.periodo = periodo
    def set_carrinho_id(self,carrinho):
        self.carrinho_id = carrinho
    def set_usuario_id(self,usuario):
        self.usuario_id = usuario
    def get_data(self):
        return(self.data)
    def get_periodo(self):
        return(self.periodo)
    def get_carrinho_id(self):
        return(self.carrinho_id)
    def get_usuario_id(self):
        return(self.usuario_id)
    

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

class Acesso:
    def __init__(self):
        self.usuario = ""
        self.nif = 0
        self.pwd = ""
    def get_usuario(self):
        return(self.usuario)
    def set_usuario(self,user):
        self.usuario = user
    def get_nif(self):
        return(self.nif)
    def set_nif(self,nif):
        self.nif = nif
    def get_pwd(self):
        return(self.pwd)
    def set_pwd(self,pwd):
        self.pwd = pwd




###############################################################################
################################################################ Instanciamento
###############################################################################
app = Flask(__name__)

disciplina = Disciplina()
usuario = Usuario()
carrinho = Carrinho()
equipamento = Equipamento()
reserva = Reserva()
calendario = Calendario()
acesso = Acesso()



###############################################################################
######################################################################### index
###############################################################################

@app.route("/")
def index():
    return render_template('index.html', userName=acesso.get_usuario())






###############################################################################
########################################################################## main
###############################################################################

@app.route("/main")
def main():
    data1 = calendario.get_data()
    sql = "SELECT id,data,periodo,carrinho_id,usuario_id FROM reserva WHERE data='{}';".format(data1)
    lista1 = db_cmd(sql)

    calendario.set_delta( calendario.get_delta()+1 )
    data2 = calendario.get_data()
    sql = "SELECT id,data,periodo,carrinho_id,usuario_id FROM reserva WHERE data='{}';".format(data2)
    lista2 = db_cmd(sql)

    calendario.set_delta( calendario.get_delta()+1 )
    data3 = calendario.get_data()
    sql = "SELECT id,data,periodo,carrinho_id,usuario_id FROM reserva WHERE data='{}';".format(data3)
    lista3 = db_cmd(sql)

    calendario.set_delta( calendario.get_delta()-2 )
    data = calendario.get_data()
    return render_template('main.html', userName=acesso.get_usuario(), lista1=lista1, data1=data1, lista2=lista2, data2=data2, lista3=lista3, data3=data3, data=data )

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
@app.route("/login")
def login():
    sql = "SELECT nif,nome FROM usuario;"
    user = db_cmd(sql)
    return render_template('login.html', user=user, userName=acesso.get_usuario() )

@app.route("/login/validar", methods=['GET','POST'])
def loginvalidar():
    if request.method == 'POST':
        acesso.set_usuario(request.form['browser'])
        acesso.set_pwd(request.form['pwd'])
        sql = "SELECT nif FROM usuario WHERE nome='{}';".format(acesso.get_usuario())
        nif = db_cmd(sql)
        acesso.set_nif( nif[0][0] )

        sql = "SELECT senha FROM usuario WHERE nif='{}';".format(acesso.get_nif() )
        senha = db_cmd(sql)
        # return "{} == {}".format( senha[0][0], acesso.get_pwd() )
        if senha[0][0] == acesso.get_pwd():
            return redirect(url_for('agendar'))
        else:
            acesso.set_usuario("")
            return redirect(url_for('loginerror'))

@app.route("/loginerror")
def loginerror():
    return render_template('login_error.html')


@app.route("/logoff")
def logoff():
    acesso.set_nif(0)
    acesso.set_pwd("")
    acesso.set_usuario("")
    return redirect(url_for('index'))


###############################################################################
####################################################################### agendar
###############################################################################
@app.route("/agendar")
def agendar():
    data = calendario.get_data()
    sql = "SELECT id,nome FROM carrinho;"
    listaCarrinhos = db_cmd(sql)
    sql = "SELECT periodo,carrinho_id,usuario_id FROM reserva where data='{}' ORDER BY carrinho_id;".format(data)
    listaReservas = db_cmd(sql)
    listaPeriodos = (['M','Matutino'],['V','Vespertino'],['N','Noturno'])
    lista = []
    achei = 0
    for p in listaPeriodos:
        for c in listaCarrinhos:
            achei = 0
            for l in listaReservas:
                if p[0]==l[0] and c[0]==l[1]:
                    achei = 1
                    break
            if not achei:
                dt = []
                # dt.append( datetime.now().strftime("%Y-%m-%d") )
                dt.append( data )
                lista.append( (dt,str(p[0]),str(c[0])) )
    return render_template('agendar.html', lista=lista, userName=acesso.get_usuario() )


@app.route("/agendar/datadec", methods=['GET','POST'])
def agendardatadec():
    calendario.set_delta( calendario.get_delta()-1 )
    return redirect(url_for('agendar'))

@app.route("/agendar/datainc", methods=['GET','POST'])
def agendardatainc():
    calendario.set_delta( calendario.get_delta()+1 )
    return redirect(url_for('agendar'))

@app.route("/agendar/carrinho/<id>/<periodo>", methods=['GET','POST'])
def agendarcarrinho(id, periodo):
    sql =  "INSERT INTO reserva (data, periodo, carrinho_id, usuario_id) VALUES ('{}','{}',{},'{}');".format(str(calendario.get_data()), str(periodo),int(id), int(acesso.get_nif()) )
    db_cmd(sql)
    return redirect(url_for('agendar'))



###############################################################################
####################################################################### excluir
###############################################################################
@app.route("/excluir")
def excluir():
    sql = "SELECT id,data,periodo,carrinho_id FROM reserva WHERE usuario_id='{}' AND data>='{}';".format(acesso.get_nif(), calendario.get_data_today() )
    lista = db_cmd(sql)
    return render_template('excluir.html', lista=lista, userName=acesso.get_usuario() )

@app.route("/excluir/<id>")
def excluir_id(id):
    sql = "DELETE FROM reserva WHERE id='{}';".format(id)
    db_cmd(sql)
    return redirect(url_for('excluir'))


###############################################################################
##################################################################### Gerenciar
###############################################################################
@app.route("/gerenciar")
def gerenciar():
    return render_template('gerenciar.html', userName=acesso.get_usuario() )



###############################################################################
######################################################### Gerenciar disciplinas
################################################################ (codigo), nome
###############################################################################
# @app.route("/gerenciar/disciplinas", methods=['GET','POST'])
# def gerenciardisciplinas(): 
#     if request.method == 'POST':
#         disciplina.set_codigo(request.form['disciplinaCodigo'])
#         disciplina.set_nome(request.form['disciplinaNome'])
#         if disciplina.get_codigo != ' ':
#             return redirect(url_for('gerenciardisciplinasadd'))
#     else:
#         sql = "SELECT * FROM disciplina;"
#         lista = db_cmd(sql)
#         return render_template('gerenciar_disciplinas.html', lista=lista, userName=acesso.get_usuario() )

# @app.route("/gerenciar/disciplinas/add")
# def gerenciardisciplinasadd():  
#     sql =  "INSERT INTO disciplina (codigo, nome) VALUES ('{}', '{}');".format(str(disciplina.get_codigo()), str(disciplina.get_nome()))
#     db_cmd(sql)
#     return redirect(url_for('gerenciardisciplinas'))

# @app.route("/gerenciar/disciplinas/del/<codigo>", methods=['GET', 'POST'])
# def gerenciardisciplinasdel(codigo):
#     sql = "DELETE FROM disciplina WHERE codigo='{}';".format(codigo)
#     db_cmd(sql)
#     return redirect(url_for('gerenciardisciplinas'))





###############################################################################
############################################################ Gerenciar usuarios
################################# (nif), nome, [disciplina]->disciplina(codigo)
###############################################################################

@app.route("/gerenciar/usuarios", methods=['GET','POST'])
def gerenciarusuarios():
    if request.method == 'POST':
        nif  = str( request.form['nif'] )
        nome = str( request.form['nome'] )
        sql =  "INSERT INTO usuario (nif, nome) VALUES ('{}','{}');".format( nif, nome )
        db_cmd(sql)
        return redirect(url_for('gerenciarusuarios'))
    else:
        sql = "SELECT id,nif,nome FROM usuario;"
        usuarios = db_cmd(sql)
        return render_template('gerenciar_usuarios.html', usuarios=usuarios, userName=acesso.get_usuario() )


@app.route("/gerenciar/usuarios/del/<id>", methods=['GET', 'POST'])
def gerenciarusuariosdel(id):
    sql = "DELETE FROM usuario WHERE id='{}';".format(id)
    db_cmd(sql)
    return redirect(url_for('gerenciarusuarios'))





###############################################################################
########################################################### Gerenciar carrinhos
################################################## (id), nome, qtd_equipamentos
###############################################################################
@app.route("/gerenciar/carrinhos", methods=['GET','POST'])
def gerenciarcarrinhos():
    if request.method == 'POST':
        carrinho.set_id(request.form['carrinhoId'])
        carrinho.set_nome(request.form['carrinhoNome'])
        return redirect(url_for('gerenciarcarrinhosadd'))
    else:
        sql = "SELECT * FROM carrinho;"
        lista = db_cmd(sql)
        return render_template('gerenciar_carrinhos.html', lista=lista, userName=acesso.get_usuario() )

@app.route("/gerenciar/carrinhos/add")
def gerenciarcarrinhosadd():
    sql =  "INSERT INTO carrinho (id, nome) VALUES ('{}','{}');".format(str(carrinho.get_id() ), str(carrinho.get_nome()))
    db_cmd(sql)
    return redirect(url_for('gerenciarcarrinhos'))

@app.route("/gerenciar/carrinhos/del/<id>", methods=['GET', 'POST'])
def gerenciarcarrinhosdel(id):
    sql = "DELETE FROM carrinho WHERE id='{}';".format(id)
    db_cmd(sql)
    return redirect(url_for('gerenciarcarrinhos'))





###############################################################################
######################################################## Gerenciar equipamentos
######################### (np), nome, carrinho, descricao, adquirido_em, status
###############################################################################
@app.route("/gerenciar/equipamentos", methods=['GET','POST'])
def gerenciarequipamentos():
    if request.method == 'POST':
        equipamento.set_np(request.form['equipNumPatr'])
        equipamento.set_nome(request.form['equipNome'])
        equipamento.set_carrinho(request.form['equipCarrinho'])
        return redirect(url_for('gerenciarequipamentosadd'))
    else:
        sql = "SELECT * FROM carrinho;"
        carrinho = db_cmd(sql)
        sql = "SELECT * FROM equipamento;"
        lista = db_cmd(sql)
        return render_template('gerenciar_equipamentos.html', lista=lista, carrinho=carrinho, userName=acesso.get_usuario())

@app.route("/gerenciar/equipamentos/add")
def gerenciarequipamentosadd():
    sql =  "INSERT INTO equipamento (np, nome, carrinho) VALUES ('{}','{}','{}');".format(str(equipamento.get_np()), str(equipamento.get_nome()), str(equipamento.get_carrinho()) )
    db_cmd(sql)
    return redirect(url_for('gerenciarequipamentos'))

@app.route("/gerenciar/equipamentos/del/<id>", methods=['GET', 'POST'])
def gerenciarequipamentosdel(id):
    sql = "DELETE FROM equipamento WHERE np='{}';".format(id)
    db_cmd(sql)
    return redirect(url_for('gerenciarequipamentos'))





###############################################################################
############################################################ Gerenciar reservas
###### (id), data, periodo, carrinho_id->carrinho(id), usuario_id->usuario(nif)
###############################################################################
@app.route("/gerenciar/reservas", methods=['GET','POST'])
def gerenciarreservas():
    if request.method == 'POST':
        reserva.set_data(request.form['calendario'])
        reserva.set_periodo(request.form['periodo'])
        reserva.set_carrinho_id(request.form['carrinho'])
        reserva.set_usuario_id(request.form['usuario'])
        return redirect(url_for('gerenciarreservasadd'))
    else:
        sql = "SELECT id,nome FROM carrinho;"
        carrinho = db_cmd(sql)
        sql = "SELECT nif,nome FROM usuario;"
        usuario = db_cmd(sql)
        sql = "SELECT * FROM reserva ORDER BY id DESC;"
        lista = db_cmd(sql)
        return render_template('gerenciar_reservas.html', lista=lista, carrinho=carrinho, usuario=usuario, userName=acesso.get_usuario())

@app.route("/gerenciar/reservas/add")
def gerenciarreservasadd():
    sql =  "INSERT INTO reserva (data, periodo, carrinho_id, usuario_id) VALUES ('{}','{}','{}','{}');".format(str(reserva.get_data()), str(reserva.get_periodo()),str(reserva.get_carrinho_id()), str(reserva.get_usuario_id()) )
    db_cmd(sql)
    return redirect(url_for('gerenciarreservas'))

@app.route("/gerenciar/reservas/del/<id>", methods=['GET', 'POST'])
def gerenciarreservasdel(id):
    sql = "DELETE FROM reserva WHERE id='{}';".format(id)
    db_cmd(sql)
    return redirect(url_for('gerenciarreservas'))



###############################################################################
################################################################# create tables
###############################################################################

@app.route("/createtables")
def createtables():
    # sql = "CREATE TABLE IF NOT EXISTS disciplina( codigo varchar(6) not null, nome varchar(50) not null, primary key(codigo));"
    # db_cmd(sql)
    # sql = "CREATE TABLE IF NOT EXISTS usuario( id SERIAL PRIMARY KEY, nif INTEGER, nome TEXT, senha TEXT );"
    sql = "CREATE TABLE IF NOT EXISTS usuario ( id SERIAL PRIMARY KEY, nif INTEGER, nome TEXT, senha TEXT );"
    db_cmd(sql)
    sql = "CREATE TABLE IF NOT EXISTS carrinho( id SERIAL PRIMARY KEY, nome TEXT );"
    db_cmd(sql)
    # sql = "CREATE TABLE IF NOT EXISTS equipamento( np INT NOT NULL, nome VARCHAR(20) NOT NULL, carrinho INT, descricao VARCHAR(50), adquirido_em DATE, status VARCHAR(16), PRIMARY KEY(np));"
    # db_cmd(sql)
    # sql = "CREATE TABLE IF NOT EXISTS reserva( id SERIAL, data DATE, periodo CHAR, carrinho_id INTEGER, usuario_id INT, PRIMARY KEY(id), FOREIGN KEY(carrinho_id) REFERENCES carrinho(id), FOREIGN KEY(usuario_id) REFERENCES usuario(nif) );"
    # db_cmd(sql)
    # sql =  "INSERT IGNORE INTO disciplina (codigo, nome) VALUES ('{}','{}');".format( "GES", "Gestão")
    # db_cmd(sql)
    sql =  "INSERT INTO usuario ( nif, nome, senha) VALUES ('{}','{}','{}');".format( 1,"Admin", "admin" )
    db_cmd(sql)

    return redirect(url_for('index'))




###############################################################################
######################################################## PI1_DB DROP ALL TABLES
###############################################################################
@app.route("/dropalltables")
def dropalltables():
    # sql = "DROP TABLE IF EXISTS reserva;"
    # db_cmd(sql)
    # sql = "DROP TABLE IF EXISTS equipamento;"
    # db_cmd(sql)
    sql = "DROP TABLE IF EXISTS carrinho;"
    db_cmd(sql)
    sql = "DROP TABLE IF EXISTS usuario;"
    db_cmd(sql)
    # sql = "DROP TABLE IF EXISTS disciplina;"
    # db_cmd(sql)
    return redirect(url_for('index'))

###############################################################################
###############################################################################

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

###############################################################################
###############################################################################
