# fastAPI-studys

"""
API simples de tarefas usando FastAPI.

Objetivo do exercício:
- Entender como uma API recebe requisições HTTP.
- Entender como criar rotas com FastAPI.
- Entender como enviar e receber dados em JSON.
- Entender como validar dados usando Pydantic.
- Entender os métodos HTTP principais: GET, POST, PUT e DELETE.

Requisitos da API:
1. Listar todas as tarefas.
2. Buscar uma tarefa pelo ID.
3. Criar uma nova tarefa.
4. Atualizar uma tarefa existente.
5. Deletar uma tarefa.
6. Listar apenas tarefas pendentes.

Como rodar:
1. Instale as dependências:
   pip install fastapi uvicorn

2. Rode o servidor:
   uvicorn main:app --reload

3. Abra a documentação automática:
   http://127.0.0.1:8000/docs
"""