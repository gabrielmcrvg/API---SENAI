# routers/cursos.py
from sqlalchemy.orm import selectinload
from fastapi import APIRouter, HTTPException, status
from database import SessionLocal
from models.curso import Curso
from schemas.curso import CursoEntrada, CursoResposta, CursoComAlunos

router = APIRouter(prefix='/cursos', tags=['Cursos'])

# =-= GET =-=

@router.get('', response_model=list[CursoResposta])
def listar_cursos():
    with SessionLocal() as session:
        return session.query(Curso).all()
    
@router.get('/{curso_id}', response_model=CursoComAlunos)
def buscar_curso(curso_id:int):
    with SessionLocal() as session:
        curso = session.query(Curso).options(selectinload(Curso.alunos)).get(curso_id) # faz uma busca na tabela cursos, me traz tambem os alunos desse curso
        if curso is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Curso não encontrado!')
        if curso.alunos:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Não é possivel realizar exclusão, Há alunos matriculados neste curso!")
        return curso

# =-= POST =-=

@router.post('', response_model=CursoResposta, status_code=201)
def criar_cursos(dados: CursoEntrada):
    with SessionLocal() as session:
        curso = Curso(**dados.model_dump())
        session.add(curso)
        session.commit()
        return curso

# =-= DELETE =-=

@router.delete('/{curso_id}')
def deletar_curso(curso_id:int):
    with SessionLocal() as session:
        curso = session.get(Curso, curso_id)
        if curso is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado")
        if curso.alunos:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="O curso tem alunos matriculados")
        session.delete(curso)
        session.commit()