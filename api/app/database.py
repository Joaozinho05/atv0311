"""Infraestrutura de acesso ao banco: conexão e criação do esquema."""
import time
from contextlib import contextmanager

import psycopg2
from psycopg2.extras import RealDictCursor

from app.config import Config

SCHEMA = """
CREATE TABLE IF NOT EXISTS alunos (
    id    SERIAL PRIMARY KEY,
    nome  VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    curso VARCHAR(100) NOT NULL
);
"""


def _conectar():
    return psycopg2.connect(
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        dbname=Config.DB_NAME,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        cursor_factory=RealDictCursor,
    )


@contextmanager
def get_cursor():
    """Abre conexão, entrega um cursor, faz commit (ou rollback) e fecha."""
    conn = _conectar()
    try:
        with conn.cursor() as cur:
            yield cur
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db(tentativas=10, espera=2):
    """Cria a tabela. Tenta de novo se o banco ainda estiver subindo."""
    for n in range(1, tentativas + 1):
        try:
            with get_cursor() as cur:
                cur.execute(SCHEMA)
            print("Banco pronto, tabela 'alunos' garantida.", flush=True)
            return
        except psycopg2.OperationalError as erro:
            print(f"Banco indisponível (tentativa {n}/{tentativas}): {erro}", flush=True)
            if n == tentativas:
                raise
            time.sleep(espera)
