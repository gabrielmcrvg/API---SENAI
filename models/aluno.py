from pydantic import BaseModel, Field

class AlunoEntrada(BaseModel):
    nome:str = Field(min_length=3)
    idade:int = Field(ge=16)
    ativo: bool = True

class AlunoResposta(BaseModel):
    id: int
    nome: str
    idade: int
    ativo: bool

class AlunoPatch(BaseModel):
    nome: str | None = Field(default=None, min_length=3)
    idade: int | None = Field(default=None, ge=16)
    ativo: bool | None = None
