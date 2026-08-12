from fastapi import APIRouter, HTTPException, status
from database import SessionLocal
from models.aluno import Aluno
from models.curso import Curso
from schemas.aluno import AlunoEntrada, AlunoEntradaSemCurso, AlunoPatch, AlunoResposta, MatriculaEmLote, AlunosComCurso
from utils.utils import obter_ou_404
from excecoes import RecursoNaoEncontrado

router = APIRouter(prefix='/alunos', tags=['Alunos'])

# =-= GET =-=

@router.get('/listar_alunos', response_model=list[AlunoResposta])
def listar_alunos(ativo: bool | None = None, limite: int = 10):
    with SessionLocal() as session:
        query = session.query(Aluno)
        if ativo is not None:
            query = query.filter(Aluno.ativo == ativo)
        # Antes o filtro era descartado porque o retorno ignorava "query"
        # e chamava session.query(Aluno).all() de novo, sem o filtro e sem o limite.
        return query.limit(limite).all()

@router.get('/{aluno_id}', response_model=AlunoResposta)
def buscar_aluno(aluno_id: int):
    with SessionLocal() as session:
        aluno = session.get(Aluno, aluno_id)
        if aluno is None:
            raise RecursoNaoEncontrado("Aluno")
        return aluno

# =-= POST =-=

@router.post("/lote/{curso_id}", response_model=list[AlunosComCurso], status_code= 201)
def criar_alunos_em_lote(curso_id: int, dados:MatriculaEmLote):
     with SessionLocal() as session:
        curso_existe = obter_ou_404(session, Curso, curso_id, "Curso")

        alunos = [Aluno(**a.model_dump()) for a in dados.alunos]
        for aluno in alunos:
            aluno.cursos.append(curso_existe)
        session.add_all(alunos)
        session.commit()
        return alunos

@router.post("/lote_varios_cursos/{curso_id}", response_model=list[AlunoResposta], status_code=201)
def criar_aluno_em_lote_cursos_diferentes(dados: list[AlunoEntrada]):
     with SessionLocal() as session:
        ids_pedidos = {d.curso_id for d in dados}
        ids_existentes = {c.id for c in session.query(Curso).filter(Curso.id.in_(ids_pedidos).all())}
        faltando = ids_pedidos - ids_existentes
        if faltando:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cursos inexistentes: {sorted(faltando)}")
        alunos = [Aluno(**d.model_dump()) for d in dados]
        session.add_all(alunos)
        session.commit()
        return alunos

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

@router.patch('/{aluno_id}', response_model=AlunoResposta)
def alterar_aluno(aluno_id: int, dados: AlunoPatch):
    with SessionLocal() as session:
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
def remover_aluno(aluno_id: int):
    with SessionLocal() as session:
        aluno = session.get(Aluno, aluno_id)
        if aluno is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Aluno não encontrado!')
        session.delete(aluno)
        session.commit()
