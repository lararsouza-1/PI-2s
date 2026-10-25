import sqlite3
from banco import CAMINHO_BANCO, criarBanco

def cadastrarProduto(nome, preco, quantidade):
    if not isinstance(nome, str) or nome.strip() == "":
        return "Nome obrigatorio"

    if preco <= 0:
        return "O preço deve ser maior que zero"

    if not isinstance(quantidade, int):
        return "A quantidade deve ser um número inteiro"

    if quantidade <= 0:
        return "A quantidade deve ser maior que zero"

    criarBanco()

    conexao = sqlite3.connect(CAMINHO_BANCO)

    try:
        cursor = conexao.cursor()

        cursor.execute("""
            INSERT INTO produtos (nome, preco, quantidade)
            VALUES (?, ?, ?)
        """, (nome.strip(), preco, quantidade))

        conexao.commit()

        return "Produto cadastrado com sucesso!"

    finally:
        
        conexao.close()


def buscarProduto(id=None, nome=None):
       if id is None and nome is None:
            return "Informe o ID ou o nome do produto"

       if id is not None and not isinstance(id, int):
        return "O ID deve ser um número inteiro"

       if id is not None and id <= 0:
            return "ID invalido"

       if id is None and (not isinstance(nome, str) or nome.strip() == ""):
            return "Nome invalido"

       criarBanco()

       conexao = sqlite3.connect(CAMINHO_BANCO)

       try:
           cursor = conexao.cursor()
           if id is not None:
               cursor.execute(
               "SELECT * FROM produtos WHERE id = ?",(id,)
               ) 

           else:
               cursor.execute(
                   "SELECT * FROM produtos WHERE nome = ?",
                   (nome.strip(),)
               )

           produto = cursor.fetchone()

           if produto is None:
               return "Produto não encontrado"

           return produto
               
       finally:
           conexao.close() 