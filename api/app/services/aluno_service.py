"""Camada de NEGÓCIO: validações e regras. Não conhece HTTP nem SQL."""
from app.exceptions import AlunoNaoEncontradoError, ValidacaoError
from app.repositories.aluno_repository import AlunoRepository


class AlunoService:
    def __init__(self, repository=None):
        self.repository = repository or AlunoRepository()

    @staticmethod
    def _validar(dados):
        if not isinstance(dados, dict):
            raise ValidacaoError("Envie um JSON com nome, email e curso.")

        limpos = {}
        for campo in ("nome", "email", "curso"):
            valor = dados.get(campo)
            if not isinstance(valor, str) or not valor.strip():
                raise ValidacaoError(f"O campo '{campo}' é obrigatório.")
            limpos[campo] = valor.strip()

        if "@" not in limpos["email"] or "." not in limpos["email"].split("@")[-1]:
            raise ValidacaoError("O campo 'email' é inválido.")
        return limpos

    def listar(self):
        return self.repository.listar()

    def buscar(self, aluno_id):
        aluno = self.repository.buscar_por_id(aluno_id)
        if aluno is None:
            raise AlunoNaoEncontradoError(aluno_id)
        return aluno

    def criar(self, dados):
        d = self._validar(dados)
        return self.repository.criar(d["nome"], d["email"], d["curso"])

    def atualizar(self, aluno_id, dados):
        d = self._validar(dados)
        aluno = self.repository.atualizar(aluno_id, d["nome"], d["email"], d["curso"])
        if aluno is None:
            raise AlunoNaoEncontradoError(aluno_id)
        return aluno

    def remover(self, aluno_id):
        if not self.repository.remover(aluno_id):
            raise AlunoNaoEncontradoError(aluno_id)
