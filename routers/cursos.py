# routers/cursos.py

from fastapi import APIRouter, HTTPException
from models.curso import CursoEntrada, CursoResposta

router = APIRouter(prefix='/cursos', tags=['Cursos'])

cursos = []

# =-= GET =-=

@router.get('', response_model=list[CursoResposta])
def listar_cursos():
    return cursos

# =-= POST =-=

@router.post('', response_model=CursoResposta, status_code=201)
def criar_cursos(curso: CursoEntrada):
    novo = curso.model_dump()
    novo['id'] = max([c['id'] for c in cursos], default=0) + 1
    cursos.append(novo)
    return novo
    
