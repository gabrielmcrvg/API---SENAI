# routers/cursos.py
from sqlalchemy.orm import selectinload
from fastapi import APIRouter, HTTPException
from database import SessionLocal
from models.curso import Curso
from schemas.curso import CursoEntrada, CursoResposta, CursoComAlunos

router = APIRouter(prefix='/cursos', tags=['Cursos'])

cursos = [{'id': 1, 'nome': 'Python', 'carga_horaria': 15},
          {'id': 2, 'nome': 'Excel', 'carga_horaria': 25}]

# =-= GET =-=

@router.get('', response_model=list[CursoResposta])
def listar_cursos():
    with SessionLocal() as session:
        return session.query(Curso).all()
    
@router.get('/{curso_id}', response_model=CursoComAlunos)
def buscar_curso(curso_id:int):
    with SessionLocal() as session:
        curso = session.query(Curso).options(selectinload(Curso.alunos)).get(curso_id)
        if curso is None:
            raise HTTPException(status_code=404, detail='Curso não encontrado!')
        return curso

# =-= POST =-=

@router.post('', response_model=CursoResposta, status_code=201)
def criar_cursos(dados: CursoEntrada):
    with SessionLocal() as session:
        curso = Curso(**dados.model_dump())
        session.add(curso)
        session.commit()
        return curso

    
