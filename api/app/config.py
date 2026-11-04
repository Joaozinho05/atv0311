"""Configuração: tudo vem de variáveis de ambiente (definidas no docker-compose)."""
import os


class Config:
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", "5432"))
    DB_NAME = os.getenv("POSTGRES_DB", "escola")
    DB_USER = os.getenv("POSTGRES_USER", "aluno")
    DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "senha123")
