
from fastapi import APIRouter, Depends, HTTPException, status

from database import SessionDep
from dependencias import Paginacao
from models.curso import Curso
from schemas.curso import CursoEntrada, CursoResposta, CursoComAlunos
from utils.utils import obter_ou_404

router = APIRouter(prefix='/cursos', tags=['Cursos'])

# =-= GET =-=

@router.get('', response_model=list[CursoResposta])
def listar_cursos(session: SessionDep, pag: Paginacao = Depends()):
    return session.query(Curso).offset(pag.skip).limit(pag.limit).all()

@router.get('/{curso_id}', response_model=CursoComAlunos)
def buscar_curso(session: SessionDep, curso_id: int):
    curso = obter_ou_404(session, Curso, curso_id, "Curso")
    return curso

# =-= POST =-=

@router.post("", response_model=list[CursoResposta], status_code=201)
def criar_cursos(session: SessionDep, dados: list[CursoEntrada]):
    cursos = [Curso(**d.model_dump()) for d in dados]
    session.add_all(cursos)
    session.commit()
    return cursos

# =-= DELETE =-=

@router.delete('/{curso_id}', status_code=status.HTTP_204_NO_CONTENT)
def deletar_curso(session: SessionDep, curso_id: int):
    curso = session.get(Curso, curso_id)
    if curso is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado")
    if curso.alunos:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="O curso tem alunos matriculados")
    session.delete(curso)
    session.commit()