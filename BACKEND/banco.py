import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

CAMINHO_BANCO = Path(__file__).resolve().parent / "banco.db"

LIMITE_ESTOQUE_BAIXO = 5

_bancoPronto = False


def criarBanco():
    global _bancoPronto

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

    cursor.execute("""
  CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    criado_em TEXT NOT NULL
)
""")

    cursor.execute("""
  CREATE TABLE IF NOT EXISTS vendas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente TEXT NOT NULL,
    produto_id INTEGER NOT NULL,
    produto TEXT NOT NULL,
    quantidade INTEGER NOT NULL,
    valor_unitario REAL NOT NULL,
    total REAL NOT NULL,
    pagamento TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'Concluída',
    data TEXT NOT NULL
)
""")

    cursor.execute("""
  CREATE TABLE IF NOT EXISTS movimentos_estoque (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produto_id INTEGER NOT NULL,
    produto TEXT NOT NULL,
    quantidade_anterior INTEGER NOT NULL,
    quantidade_nova INTEGER NOT NULL,
    motivo TEXT NOT NULL DEFAULT '',
    criado_em TEXT NOT NULL
)
""")

    cursor.execute("""
  CREATE TABLE IF NOT EXISTS notificacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    texto TEXT NOT NULL,
    lida INTEGER NOT NULL DEFAULT 0,
    criada_em TEXT NOT NULL
)
""")

    # Só existe uma linha de configurações (id = 1)
    cursor.execute("""
  CREATE TABLE IF NOT EXISTS configuracoes (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    nome_loja TEXT NOT NULL,
    email TEXT NOT NULL,
    avisos_email INTEGER NOT NULL DEFAULT 1,
    alerta_estoque INTEGER NOT NULL DEFAULT 1
)
""")
    cursor.execute("""
  INSERT OR IGNORE INTO configuracoes (id, nome_loja, email, avisos_email, alerta_estoque)
  VALUES (1, 'Anvellis', 'contato@anvellis.com', 1, 1)
""")

    conexao.commit()
    conexao.close()
    _bancoPronto = True


@contextmanager
def conexaoBanco():
    """Abre o banco, salva (commit) se tudo deu certo e sempre fecha no final.

    Uso:
        with conexaoBanco() as conexao:
            conexao.execute(...)
    """
    if not _bancoPronto:
        criarBanco()

    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.row_factory = sqlite3.Row
    try:
        yield conexao
        conexao.commit()
    except Exception:
        conexao.rollback()
        raise
    finally:
        conexao.close()


def agoraUTC():
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def plural(n, singular, pluralTxt):
    return f"{n} {singular if n == 1 else pluralTxt}"


def criarNotificacao(conexao, titulo, texto):
    conexao.execute(
        "INSERT INTO notificacoes (titulo, texto, lida, criada_em) VALUES (?, ?, 0, ?)",
        (titulo, texto, agoraUTC()),
    )


def avisarEstoqueBaixo(conexao, nome, quantidade):
    """Cria a notificação de estoque baixo/zerado (se o alerta estiver ligado nas configurações)."""
    config = conexao.execute("SELECT alerta_estoque FROM configuracoes WHERE id = 1").fetchone()
    if config is not None and not config["alerta_estoque"]:
        return

    if quantidade == 0:
        criarNotificacao(conexao, "Produto sem estoque", f"{nome} está sem estoque.")
    elif quantidade <= LIMITE_ESTOQUE_BAIXO:
        criarNotificacao(
            conexao,
            "Estoque baixo",
            f"{nome} tem apenas {plural(quantidade, 'unidade', 'unidades')} em estoque.",
        )


if __name__ == "__main__":
    criarBanco()
