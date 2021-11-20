import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())


cur = connection.cursor()
cur.execute("INSERT INTO usuario (nif,nome,senha) VALUES ({},'{}','{}')".format(1,'Admin','admin') )
connection.commit()
connection.close()
