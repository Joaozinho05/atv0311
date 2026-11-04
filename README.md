# CRUD de Alunos em camadas (Flask + PostgreSQL + Docker Compose)

API REST simples para cadastrar alunos, com arquitetura em camadas e banco de dados em container.

## Arquitetura em camadas

```
Cliente HTTP
    |
    v
controllers/aluno_controller.py   -> APRESENTAÇÃO: rotas HTTP, status codes
    |
    v
services/aluno_service.py         -> NEGÓCIO: validações e regras
    |
    v
repositories/aluno_repository.py  -> PERSISTÊNCIA: único lugar com SQL
    |
    v
database.py -> PostgreSQL (container db)
```

Apoio: `models/aluno.py` (entidade), `exceptions.py` (erros de domínio), `config.py` (variáveis de ambiente), `main.py` (monta a aplicação).

## Containers

| Serviço | Imagem        | Função                      |
|---------|---------------|-----------------------------|
| db      | postgres:16   | banco, com volume `db_data` |
| api     | build ./api   | API Flask (gunicorn), porta 5000 |

A API acessa o banco pelo nome do serviço (`DB_HOST=db`). O `depends_on` com `healthcheck` garante que a API só sobe depois que o Postgres estiver pronto.

## Como rodar

```bash
docker compose up --build -d
docker compose ps
docker compose logs api
```

## Endpoints

| Método | Rota          | Ação              | Sucesso |
|--------|---------------|-------------------|---------|
| GET    | /health       | verificar a API   | 200     |
| GET    | /alunos       | listar            | 200     |
| GET    | /alunos/{id}  | buscar um         | 200     |
| POST   | /alunos       | criar             | 201     |
| PUT    | /alunos/{id}  | atualizar         | 200     |
| DELETE | /alunos/{id}  | remover           | 204     |

Erros: 400 (dados inválidos), 404 (não encontrado), 409 (e-mail duplicado).

## Testando com curl

```bash
curl http://localhost:5000/health

curl -X POST http://localhost:5000/alunos \
  -H "Content-Type: application/json" \
  -d '{"nome":"Ana","email":"ana@escola.com","curso":"ADS"}'

curl http://localhost:5000/alunos
curl http://localhost:5000/alunos/1

curl -X PUT http://localhost:5000/alunos/1 \
  -H "Content-Type: application/json" \
  -d '{"nome":"Ana Paula","email":"ana@escola.com","curso":"ADS"}'

curl -X DELETE http://localhost:5000/alunos/1
```

No PowerShell do Windows, use `curl.exe` no lugar de `curl` e aspas duplas escapadas no JSON, ou teste pelo Postman/Insomnia.

## Verificando o banco dentro do container

```bash
docker compose exec db psql -U aluno -d escola -c "SELECT * FROM alunos;"
```

## Provando a persistência

```bash
docker compose down        # remove containers, mantém o volume
docker compose up -d
curl http://localhost:5000/alunos   # os dados continuam lá
```

## Encerrar

```bash
docker compose down        # mantém os dados
docker compose down -v     # apaga também o volume
```
