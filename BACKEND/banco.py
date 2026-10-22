import sqlite3
from pathlib import Path

CAMINHO_BANCO = Path(__file__).resolve().parent / "banco.db"

def criarBanco():

    conexao = sqlite3.connect(CAMINHO_BANCO)
    cursor = conexao.cursor()


    cursor.execute("""
  CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    preco REAL NOT NULL,
    quantidade INTEGER NOT NULL
)
""")

    conexao.commit()
    conexao.close()

if __name__ == "__main__":
    criarBanco() 