# routers/cursos.py

from fastapi import APIRouter, HTTPException
from schemas.curso import CursoEntrada, CursoResposta

router = APIRouter(prefix='/cursos', tags=['Cursos'])

cursos = [{'id': 1, 'nome': 'Python', 'carga_horaria': 15},
          {'id': 2, 'nome': 'Excel', 'carga_horaria': 25}]

# =-= GET =-=

@router.get('', response_model=list[CursoResposta])
def listar_cursos():
    return cursos

@router.get('/{curso_id}', response_model=CursoResposta)
def buscar_curso(curso_id:int):
    for curso in cursos:
        if curso['id'] == curso_id:
            return curso
    raise HTTPException(status_code=404, detail='Curso não encontrado!')

# =-= POST =-=

@router.post('', response_model=CursoResposta, status_code=201)
def criar_cursos(curso: CursoEntrada):
    novo = curso.model_dump()
    novo['id'] = max([c['id'] for c in cursos], default=0) + 1
    cursos.append(novo)
    return novo

    
