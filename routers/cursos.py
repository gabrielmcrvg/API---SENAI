
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import selectinload

from database import SessionDep
from models.curso import Curso
from schemas.curso import CursoEntrada, CursoResposta, CursoComAlunos
from dependencias import Paginacao
from seguranca import AdminAtual, UsuarioAtual
from utils.utils import obter_ou_404, bad_request


router = APIRouter(prefix="/cursos", tags=["Cursos"])

cursos = [
    {"nome": "Python Back-End", "carga_horaria": 180},
    {"nome": "Desenvolvimento Front-End", "carga_horaria": 160},
    {"nome": "Banco de Dados com MySQL", "carga_horaria": 32},
    {"nome": "DevOps e Cloud", "carga_horaria": 120},
    {"nome": "Análise de Dados", "carga_horaria": 90},
]

@router.get("",response_model=list[CursoResposta])
def listar_cursos(session: SessionDep, pag: Paginacao =Depends()):
        return session.query(Curso).offset(pag.skip).limit(pag.limit).all()
    
@router.get("/{curso_id}", response_model=CursoComAlunos)
def buscar_curso(curso_id: int, session: SessionDep, usuario: UsuarioAtual):
        curso = session.query(Curso).options(selectinload(Curso.alunos)).get(curso_id)
        if curso is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado!")
        return curso

@router.post("/{curso_id}", response_model=list[CursoResposta], status_code=201)
def criar_curso(dados: list[CursoEntrada], session: SessionDep, usuario: AdminAtual):
        cursos = [Curso(**d.model_dump()) for d in dados]
        session.add_all(cursos)
        session.commit()
        return cursos

@router.delete("/{curso_id}")
def deletar_curso(curso_id: int, session: SessionDep, usuario: AdminAtual):
        curso = session.get(Curso, curso_id)
        if curso is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "Curso inexistente!")
        if curso.alunos:
            raise HTTPException(status_code=409, detail="O curso possui alunos matriculados!")
        session.delete(curso)
        session.commit()
        return {"Mensagem": "Curso removido"}