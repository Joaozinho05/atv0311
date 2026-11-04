"""Camada de MODELO: representa o dado do domínio."""
from dataclasses import dataclass, asdict


@dataclass
class Aluno:
    id: int
    nome: str
    email: str
    curso: str

    def to_dict(self):
        return asdict(self)
