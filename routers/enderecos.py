from fastapi import APIRouter
from services.cep import consultar_cep

router = APIRouter(prefix="/enderecos", tags=["Enderecos"])

@router.get("/{cep}")
def buscar_endereco(cep: str):
    return consultar_cep(cep)