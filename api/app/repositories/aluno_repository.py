"""Camada de PERSISTÊNCIA: único lugar que conhece SQL."""
from psycopg2 import errors

from app.database import get_cursor
from app.exceptions import EmailDuplicadoError
from app.models.aluno import Aluno


def _para_aluno(row):
    return Aluno(id=row["id"], nome=row["nome"], email=row["email"], curso=row["curso"])


class AlunoRepository:
    def listar(self):
        with get_cursor() as cur:
            cur.execute("SELECT id, nome, email, curso FROM alunos ORDER BY id;")
            return [_para_aluno(r) for r in cur.fetchall()]

    def buscar_por_id(self, aluno_id):
        with get_cursor() as cur:
            cur.execute(
                "SELECT id, nome, email, curso FROM alunos WHERE id = %s;", (aluno_id,)
            )
            row = cur.fetchone()
            return _para_aluno(row) if row else None

    def criar(self, nome, email, curso):
        try:
            with get_cursor() as cur:
                cur.execute(
                    "INSERT INTO alunos (nome, email, curso) VALUES (%s, %s, %s) "
                    "RETURNING id, nome, email, curso;",
                    (nome, email, curso),
                )
                return _para_aluno(cur.fetchone())
        except errors.UniqueViolation:
            raise EmailDuplicadoError(email)

    def atualizar(self, aluno_id, nome, email, curso):
        try:
            with get_cursor() as cur:
                cur.execute(
                    "UPDATE alunos SET nome = %s, email = %s, curso = %s "
                    "WHERE id = %s RETURNING id, nome, email, curso;",
                    (nome, email, curso, aluno_id),
                )
                row = cur.fetchone()
                return _para_aluno(row) if row else None
        except errors.UniqueViolation:
            raise EmailDuplicadoError(email)

    def remover(self, aluno_id):
        with get_cursor() as cur:
            cur.execute("DELETE FROM alunos WHERE id = %s;", (aluno_id,))
            return cur.rowcount > 0
