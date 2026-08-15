from pydantic import BaseModel, ConfigDict, Field

class UsuarioEntrada(BaseModel):
    username: str = Field(min_length=3)
    password: str = Field(min_length=6)

class UsuarioResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str

class Token(BaseModel):
    access_token: str
    token_type: str