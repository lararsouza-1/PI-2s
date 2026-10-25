import sqlite3
import math
from banco import CAMINHO_BANCO, criarBanco

def cadastrarProduto(nome, preco, quantidade):
    if not isinstance(nome, str) or nome.strip() == "":
        return "Nome obrigatorio"

    if type(preco) not in (int, float) or not math.isfinite(preco):
        return "O preço deve ser numérico e válido"

    if preco <= 0:
        return "O preço deve ser maior que zero"

    if type(quantidade) is not int:
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

    if id is not None:
        if type(id) is not int or id <= 0:
            return "ID inválido"

    if id is None:
        if not isinstance(nome, str) or nome.strip() == "":
            return "Nome inválido"

    criarBanco()

    conexao = sqlite3.connect(CAMINHO_BANCO)

    try:
        cursor = conexao.cursor()

        if id is not None:
            cursor.execute(
                "SELECT * FROM produtos WHERE id = ?",
                (id,)
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

def listarProdutos():
    criarBanco()

    conexao = sqlite3.connect(CAMINHO_BANCO)

    try:
        cursor = conexao.cursor()

        cursor.execute("SELECT * FROM produtos")

        produtos = cursor.fetchall()

        return produtos

    finally:
        conexao.close()

def alterarProduto(id,novoNome,novoPreco):
    if type(id) is not int or id <= 0:
        return "ID inválido"
    
    if not isinstance(novoNome,str) or novoNome.strip() == "":
        return "Nome Invalido"

    if type(novoPreco) not in (int, float) or not math.isfinite(novoPreco):
        return "O preço deve ser numérico e válido"

    if novoPreco <= 0:
        return "O preço tem que ser maior que 0"

    criarBanco()

    conexao = sqlite3.connect(CAMINHO_BANCO)

    try:
        cursor = conexao.cursor()

        cursor.execute(""" 
        UPDATE produtos
        SET nome = ?, preco = ?
        WHERE id = ?
        """, (novoNome.strip(),novoPreco, id))

        if cursor.rowcount == 0:
            return "Produto não encontrado"

        conexao.commit()

        return "Produto alterado com sucesso!"

    finally:
        conexao.close()

def excluirProduto(id):
    if type(id) is not int or id <= 0:
        return "ID invalido!"

    criarBanco()

    conexao = sqlite3.connect(CAMINHO_BANCO)

    try:
        cursor = conexao.cursor()

        cursor.execute(
        "DELETE FROM produtos WHERE id = ?",
        (id,)
        )

        if cursor.rowcount == 0:
            return "Produto não encontrado"

        conexao.commit()

        return "Produto excluido com sucesso!"

    finally:
        conexao.close()    


def atualizarEstoque(id,novaQuantidade):
    if type(id) is not int or id <= 0:
        return "ID invalido"

    if type(novaQuantidade) is not int:
        return "A quantidade deve ser um numero inteiro!"

    if novaQuantidade < 0:
        return "A quantidade não pode ser negativa"

    criarBanco()

    conexao = sqlite3.connect(CAMINHO_BANCO)

    try:
        cursor = conexao.cursor()

        cursor.execute(
        "UPDATE produtos SET quantidade = ? WHERE id = ?",
        (novaQuantidade,id)
    )

        if cursor.rowcount == 0:
            return "Produto não encontrado"

        conexao.commit()

        return "Produto atualizado com sucesso!"

    finally:
        conexao.close()





print(atualizarEstoque(9999, 10))