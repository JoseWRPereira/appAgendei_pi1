DROP TABLE IF EXISTS reserva;
DROP TABLE IF EXISTS carrinho;
DROP TABLE IF EXISTS usuario;

    
CREATE TABLE IF NOT EXISTS usuario( 
    nif INT NOT NULL, 
    nome VARCHAR(40) NOT NULL, 
    senha VARCHAR(40), 
    PRIMARY KEY(nif)
    );

CREATE TABLE IF NOT EXISTS carrinho(
    id INT NOT NULL, 
    nome VARCHAR(16) NOT NULL,
    PRIMARY KEY(id)
    );


CREATE TABLE IF NOT EXISTS reserva(
    id INT NOT NULL, 
    calendario VARCHAR(10),
    periodo CHAR,
    carrinho_id INT, 
    usuario_id INT, 
    PRIMARY KEY(id)
    -- FOREIGN KEY(carrinho_id) REFERENCES carrinho(id), 
    -- FOREIGN KEY(usuario_id) REFERENCES usuario(nif) 
    );
