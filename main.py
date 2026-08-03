from fastapi import FastAPI, HTTPException

alunos = [
{'id': 1, 'nome': 'Gabriel', 'ativo': True},
{'id': 2, 'nome': 'Joao', 'ativo': True},
{'id': 3, 'nome': 'Pedro', 'ativo': False}
]

app = FastAPI()

@app.get('/') # quando chegar um .get na rota (''/'')...

def raiz(): # ...me devolva um dicionario
    return {'Mensagem': 'API de Escola no ar'}

@app.get('/status')

def status():
    return {'status': 'OK', 'Versão': '1.0'}

@app.get('/alunos')

def listar_alunos(ativo:bool | None = None, limite:int=10):
    resultado = alunos
    if ativo is not None:
        resultado = [a for a in resultado if a['ativo'] == ativo]
    return resultado[:limite]

@app.get('/alunos/{aluno_id}')
def buscar_aluno(aluno_id:int):
    for aluno in alunos:
        if aluno['id'] == aluno_id:
            return aluno
    raise HTTPException(status_code=404, detail='Aluno não encontrado!')

# =-= POST =-=

@app.post('/alunos', status_code=201)
def criar_aluno(aluno: dict):
    alunos.append(aluno)
    return aluno

# =-= PUT =-=

@app.put('/alunos/{aluno_id}')
def atualizar_aluno(aluno_id: int, dados: dict):
    for indice, aluno in enumerate(alunos):
        if aluno['id'] == aluno_id:
            dados['id'] = aluno_id
            alunos[indice] = dados
            return dados
    raise HTTPException(status_code=404, detail='Aluno não encontrado!')

# =-= PATCH =-=

@app.patch('/alunos/{aluno_id}')
def atualizar_aluno(aluno_id: int, dados: dict):
    for indice, aluno in enumerate(alunos):
        if aluno['id'] == aluno_id:
            aluno.update(dados)
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