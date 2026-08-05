# schemas = validação

from pydantic import BaseModel, Field

class CursoEntrada(BaseModel):
    nome:str = Field(min_length=5)
    carga_horaria:int = Field(gt=0) # greater than = maior que

class CursoResposta(BaseModel):
    id:int
    nome:str
    carga_horaria:int