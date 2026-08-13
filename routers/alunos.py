from fastapi import APIRouter, Depends, HTTPException, status
from database import SessionDep
from dependencias import Paginacao
from excecoes import RecursoNaoEncontrado
from models.aluno import Aluno
from models.curso import Curso
from schemas.aluno import AlunoEntrada, AlunoPatch, AlunoResposta, MatriculaEmLote, AlunosComCurso
from utils.utils import obter_ou_404

router = APIRouter(prefix='/alunos', tags=['Alunos'])

# =-= GET =-=

@router.get('/listar_alunos', response_model=list[AlunoResposta])
def listar_alunos(session: SessionDep, pag: Paginacao = Depends(), ativo: bool | None = None):
    query = session.query(Aluno)
    if ativo is not None:
        query = query.filter(Aluno.ativo == ativo)
    return session.query(Aluno).offset(pag.skip).limit(pag.limit).all()

@router.get('/{aluno_id}', response_model=AlunoResposta)
def buscar_aluno(session: SessionDep, aluno_id: int):
    aluno = session.get(Aluno, aluno_id)
    if aluno is None:
        raise RecursoNaoEncontrado("Aluno")
    return aluno

# =-= POST =-=

@router.post("/criar_aluno", response_model=AlunoResposta, status_code=status.HTTP_201_CREATED)
def criar_aluno(session: SessionDep, dados: AlunoEntrada):
    curso_existe = obter_ou_404(session, Curso, dados.curso_id, "Curso")
    aluno = Aluno(**dados.model_dump())
    aluno.cursos.append(curso_existe)
    session.add(aluno)
    session.commit()
    return aluno

@router.post("/lote/{curso_id}", response_model=list[AlunosComCurso], status_code=status.HTTP_201_CREATED)
def criar_alunos_em_lote(session: SessionDep, curso_id: int, dados: MatriculaEmLote):
    curso_existe = obter_ou_404(session, Curso, curso_id, "Curso")
    alunos = [Aluno(**a.model_dump()) for a in dados.alunos]
    for aluno in alunos:
        aluno.cursos.append(curso_existe)
    session.add_all(alunos)
    session.commit()
    return alunos

# =-= PUT =-= TROCA TODOS DADOS

@router.put('/{aluno_id}', response_model=AlunoResposta)
def atualizar_aluno(session: SessionDep, aluno_id: int, dados: AlunoEntrada):
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

@router.patch('/{aluno_id}', response_model=AlunoResposta)
def alterar_aluno(session: SessionDep, aluno_id: int, dados: AlunoPatch):
    aluno = session.get(Aluno, aluno_id)
    if aluno is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Aluno não encontrado!')
    mudancas = dados.model_dump(exclude_unset=True)
    for campo, valor in mudancas.items():
        setattr(aluno, campo, valor)
    session.commit()
    return aluno

# =-= DELETE =-=

@router.delete('/{aluno_id}', status_code=status.HTTP_204_NO_CONTENT)
def remover_aluno(session: SessionDep, aluno_id: int):
    aluno = session.get(Aluno, aluno_id)
    if aluno is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Aluno não encontrado!')
    session.delete(aluno)
    session.commit()