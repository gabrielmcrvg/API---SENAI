from fastapi import FastAPI
from fastapi.responses import JSONResponse
from routers import alunos, cursos, auth
from models import aluno, curso, usuario
from excecoes import RecursoNaoEncontrado



app = FastAPI(title="API - SENAI")

app.include_router(alunos.router)
app.include_router(cursos.router)
app.include_router(auth.router)

@app.get("/raiz")
def raiz():
    return {"Mensagem": "API da Escola no ar!"}

@app.get("/status")
def status():
    return{"status":"OK", "Versão":"1.0"}

@app.exception_handler(RecursoNaoEncontrado)
def tratar_nao_encontrado(request, exc):
    return JSONResponse(status_code=404,
                        content={"detail":f"{exc.recurso} nao encontrado!"})