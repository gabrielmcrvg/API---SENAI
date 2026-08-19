import httpx
from fastapi import HTTPException, status

def consultar_cep(cep: str) -> dict:
    url = f"https://viacep.com.br/ws/{cep}/json/"
    try:
        resposta = httpx.get(url, timeout=10)
    except httpx.RequestError:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Serviço de CEP indisponível")
    if resposta.status_code != 200:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Serviço de CEP indisponível")
    dados = resposta.json()
    if dados.get("erro"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CEP não encontrado")
    return dados