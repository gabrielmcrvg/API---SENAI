# schemas = validação

from pydantic import BaseModel, ConfigDict, Field

class CursoEntrada(BaseModel):
    nome:str = Field(min_length=5)
    carga_horaria:int = Field(gt=0) # greater than = maior que

class CursoResposta(BaseModel):
    id:int
    nome:str
    carga_horaria:int

class AlunoResumo(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:int
    nome:str

class CursoComAlunos(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:int
    nome:str
    carga_horaria:int
    alunos: list[AlunoResumo] = []