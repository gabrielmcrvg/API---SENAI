from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

alunos = [
{'id': 1, 'nome': 'Gabriel','idade': 23, 'ativo': True},
{'id': 2, 'nome': 'Joao','idade': 25, 'ativo': False},
{'id': 3, 'nome': 'Pedro','idade': 29, 'ativo': True},
]

app = FastAPI()

class AlunoEntrada(BaseModel):
    nome:str = Field(min_length=3)
    idade:int = Field(ge=16)
    ativo: bool = True

class AlunoResposta(BaseModel):
    id: int
    nome: str
    idade: int
    ativo: bool

class AlunoPatch(BaseModel):
    nome: str | None = Field(default=None, min_length=3)
    idade: int | None = Field(default=None, ge=16)
    ativo: bool | None = None

# =-= GET =-=

@app.get('/') # quando chegar um .get na rota (''/'')...

def raiz(): # ...me devolva um dicionario
    return {'Mensagem': 'API de Escola no ar'}

@app.get('/status')

def status():
    return {'status': 'OK', 'Versão': '1.0'}

@app.get('/alunos', response_model=list[AlunoResposta])

def listar_alunos(ativo:bool | None = None, limite:int=10):
    resultado = alunos
    if ativo is not None:
        resultado = [a for a in resultado if a['ativo'] == ativo]
    return resultado[:limite]

@app.get('/alunos/{aluno_id}', response_model=AlunoResposta)
def buscar_aluno(aluno_id:int):
    for aluno in alunos:
        if aluno['id'] == aluno_id:
            return aluno
    raise HTTPException(status_code=404, detail='Aluno não encontrado!')

# =-= POST =-=

@app.post('/alunos', status_code=201)
def criar_aluno(aluno: AlunoEntrada):
    novo = aluno.model_dump()
    novo['id'] = max([a['id'] for a in alunos], default=0) + 1
    alunos.append(novo)
    return novo

# =-= PUT =-=

@app.put('/alunos/{aluno_id}')
def atualizar_aluno(aluno_id: int, dados: AlunoEntrada):
    for indice, aluno in enumerate(alunos): # indice = posição, aluno = dicionario
        if aluno['id'] == aluno_id:
            atualizado = dados.model_dump()
            atualizado['id'] = aluno_id
            alunos[indice] = atualizado
            return atualizado
    raise HTTPException(status_code=404, detail='Aluno não encontrado!')

# =-= PATCH =-=

@app.patch('/alunos/{aluno_id}')
def alterar_aluno(aluno_id: int, dados: AlunoPatch):
    for aluno in alunos:
        if aluno['id'] == aluno_id:
            mudancas = dados.model_dump(exclude_unset=True) # exclude unset só mexe no que eu pedi pra mexer, ignora o resto
            aluno.update(mudancas)
            return aluno
    raise HTTPException(status_code=404, detail='Aluno não encontrado!')

# =-= DELETE =-=

@app.delete('/alunos/{aluno_id}')
def remover_aluno(aluno_id: int):
    for indice, aluno in enumerate(alunos):
        if aluno['id'] == aluno_id:
            alunos.pop(indice)
            return {'mensagem': 'Aluno removido'}
    raise HTTPException(status_code=404, detail='Aluno não encontrado!')