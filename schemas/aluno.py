from pydantic import BaseModel, Field, ConfigDict

class AlunoEntrada(BaseModel):
    nome: str = Field(min_length=3)
    idade: int = Field(ge=16)
    ativo: bool = True
    curso_id: int

class AlunoResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nome: str
    idade: int
    ativo: bool

class AlunoPatch(BaseModel):
    nome: str | None = Field(default=None, min_length=3)
    idade: int | None = Field(default=None, ge=16)
    ativo: bool | None = None

class CursoResumo(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nome: str

class AlunosComCurso(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nome: str
    ativo: bool
    cursos: list[CursoResumo] = []

class AlunoEntradaLote(BaseModel):
    nome: str = Field(min_length=3)
    idade: int = Field(ge=16)
    ativo: bool = True

class MatriculaEmLote(BaseModel):
    alunos: list[AlunoEntradaLote]