from pydantic import BaseModel, EmailStr, Field, ConfigDict

class AlunoEntrada(BaseModel):
    nome: str = Field(min_length=3, description="Nome completo do aluno", examples=["Ana Souza"])
    idade: int = Field(ge=16, description="Idade(mínimo 16 anos)")
    ativo: bool = True
    email: EmailStr

class AlunoEntradaLote(BaseModel):
    nome: str = Field(min_length=3)
    idade: int = Field(ge=16)
    ativo: bool = True
    email: EmailStr
    
class MatriculaEmLote(BaseModel):
    alunos: list[AlunoEntradaLote]

class AlunoResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nome: str
    idade: int
    ativo: bool
    email: EmailStr

class AlunoPatch(BaseModel):
    nome: str | None = Field(default=None, min_length=3)
    idade: int | None = Field(default=None, ge=16)
    ativo: bool | None = None
    email: EmailStr


class CursoResumo(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nome: str

class AlunosComCurso(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nome: str
    ativo: bool
    email: EmailStr
    cursos: list[CursoResumo] = []

