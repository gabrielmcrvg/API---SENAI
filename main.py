from fastapi import FastAPI
from fastapi.responses import JSONResponse
from routers import alunos, cursos
from models.aluno import Aluno
from models.curso import Curso
from excecoes import RecursoNaoEncontrado

app = FastAPI(title='API - SENAI', tags=['Status da Aplicação'])

app.include_router(alunos.router)
app.include_router(cursos.router)

@app.get('')
def raiz():
    return {'Mensagem': 'API de Escola no ar'}

@app.get('/status')
def status():
    return {'status': 'OK', 'Versão': '1.0'}

@app.exception_handler(RecursoNaoEncontrado)
def tratar_nao_encontrado(request, exc):
    return JSONResponse(status_code=404, content=tratar_nao_encontrado, detail={"Mensagem": "Objeto não encontrado"})