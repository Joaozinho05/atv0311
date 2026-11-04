"""Ponto de entrada: monta a aplicação e traduz erros de domínio em respostas HTTP."""
from flask import Flask, jsonify

from app.controllers import aluno_controller
from app.database import init_db
from app.exceptions import AlunoNaoEncontradoError, EmailDuplicadoError, ValidacaoError


def create_app():
    app = Flask(__name__)
    app.register_blueprint(aluno_controller.bp)

    @app.get("/")
    def raiz():
        return jsonify(mensagem="API de alunos no ar. Use /alunos", saude="/health")

    @app.get("/health")
    def health():
        return jsonify(status="ok")

    @app.errorhandler(ValidacaoError)
    def _400(e):
        return jsonify(erro=str(e)), 400

    @app.errorhandler(AlunoNaoEncontradoError)
    def _404(e):
        return jsonify(erro="Aluno não encontrado."), 404

    @app.errorhandler(EmailDuplicadoError)
    def _409(e):
        return jsonify(erro="E-mail já cadastrado."), 409

    init_db()
    return app


app = create_app()
