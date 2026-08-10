from fastapi import APIRouter, HTTPException, status
from database import SessionLocal
from models.aluno import Aluno
from models.curso import Curso
from schemas.aluno import AlunoEntrada, AlunoPatch, AlunoResposta
from utils.utils import obter_ou_404
from excecoes import RecursoNaoEncontrado

router = APIRouter(prefix='/alunos', tags=['Alunos'])

# =-= GET =-=

@router.get('/listar_alunos', response_model=list[AlunoResposta])
def listar_alunos(ativo:bool | None = None, limite:int=10):
    with SessionLocal() as session:
        query = session.query(Aluno)
        if ativo is not None:
            query = query.filter(Aluno.ativo == ativo)
        return session.query(Aluno).all()

@router.get('/{aluno_id}', response_model=AlunoResposta)
def buscar_aluno(aluno_id:int):
    with SessionLocal() as session:
        aluno = session.get(Aluno, aluno_id)
        if aluno is None:
            raise RecursoNaoEncontrado("Aluno")
        return aluno

# =-= POST =-=

@router.post('/criar_aluno', response_model=AlunoResposta, status_code=status.HTTP_201_CREATED)
def criar_aluno(dados: AlunoEntrada):
    with SessionLocal() as session:
        curso = session.get(Curso, dados.curso_id)
        if curso is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso informado não existe!")
        aluno = Aluno(**dados.model_dump())
        session.add(aluno)
        session.commit() # pra gravar de fato o objeto na lista
        return aluno
    
# =-= PUT =-= TROCA TODOS DADOS

@router.put('/{aluno_id}', response_model=AlunoResposta)
def atualizar_aluno(aluno_id: int, dados: AlunoEntrada):
    with SessionLocal() as session:
        aluno = session.get(Aluno, aluno_id)
        if aluno is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Aluno não encontrado!')
        aluno.nome = dados.nome
        aluno.idade = dados.idade
        aluno.ativo = dados.ativo
        aluno.curso_id = dados.curso_id
        session.commit()
        return aluno

# =-= PATCH =-= TROCA UM DADO ESPECIFICO

@router.patch('/{aluno_id}')
def alterar_aluno(aluno_id: int, dados: AlunoPatch):
    with SessionLocal() as session:
        aluno = session.get(Aluno, aluno_id)
        if aluno is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Aluno não encontrado!')
        mudancas = dados.model_dump(exclude_unset=True)
        for campo, valor in mudancas.item():
            setattr(aluno, campo, valor)
        session.commit()
        return aluno

# =-= DELETE =-=

@router.delete('/{aluno_id}', status_code=status.HTTP_204_NO_CONTENT)
def remover_aluno(aluno_id: int):
    with SessionLocal() as session:
        aluno = session.get(Aluno, aluno_id)
        if aluno is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Aluno não encontrado!')
        session.delete(aluno)
        session.commit()
        return {'Mensagem': 'Aluno removido com sucesso!'}