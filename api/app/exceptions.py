"""Erros de domínio. Cada camada fala a mesma 'língua' sem vazar detalhes do banco."""


class ValidacaoError(Exception):
    """Dados de entrada inválidos (vira HTTP 400)."""


class AlunoNaoEncontradoError(Exception):
    """Aluno não existe (vira HTTP 404)."""


class EmailDuplicadoError(Exception):
    """E-mail já cadastrado (vira HTTP 409)."""
