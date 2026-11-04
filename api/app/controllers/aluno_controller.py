"""Camada de APRESENTAÇÃO: rotas HTTP. Traduz requisição/resposta, sem regra de negócio."""
from flask import Blueprint, jsonify, request

from app.services.aluno_service import AlunoService

bp = Blueprint("alunos", __name__, url_prefix="/alunos")
service = AlunoService()


@bp.get("")
def listar():
    return jsonify([a.to_dict() for a in service.listar()])


@bp.get("/<int:aluno_id>")
def buscar(aluno_id):
    return jsonify(service.buscar(aluno_id).to_dict())


@bp.post("")
def criar():
    aluno = service.criar(request.get_json(silent=True))
    return jsonify(aluno.to_dict()), 201


@bp.put("/<int:aluno_id>")
def atualizar(aluno_id):
    aluno = service.atualizar(aluno_id, request.get_json(silent=True))
    return jsonify(aluno.to_dict())


@bp.delete("/<int:aluno_id>")
def remover(aluno_id):
    service.remover(aluno_id)
    return "", 204
