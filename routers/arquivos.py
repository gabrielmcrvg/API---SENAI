from pathlib import Path
import shutil

from fastapi import APIRouter, HTTPException, UploadFile, status
from seguranca import UsuarioAtual

router = APIRouter(prefix="/arquivos", tags=["Arquivos"])

PASTA_UPLOAD = Path("uploads")

PASTA_UPLOAD.mkdir(exist_ok=True)

TIPOS_PERMITIDOS = {"image/jpeg", "image/png"}

TAMANHO_MAXIMO = 5 * 1024 * 1024 # 5 MB

@router.post("/uploads", status_code=status.HTTP_201_CREATED)
def uploads(arquivo: UploadFile, usuario: UsuarioAtual):
    if arquivo.content_type not in TIPOS_PERMITIDOS:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tipo nao permitido. Envie JPEG OU PNG")
    if arquivo.size is not None and arquivo.size > TAMANHO_MAXIMO:
        raise HTTPException(status_code=status.HTTP_413_CONTENT_TOO_LARGE, detail="Arquivo muito grande (max 5 MB)")
    if arquivo.filename is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Arquivo sem nome")
    nome_seguro = Path(arquivo.filename).name
    destino = PASTA_UPLOAD/nome_seguro
    with open(destino, "wb") as buffer:
        shutil.copyfileobj(arquivo.file, buffer)
    return{"arquivo": arquivo.filename}

@router.post("/upload-varios", status_code=201)
def upload_varios(arquivos: list[UploadFile], usuario: UsuarioAtual):
    salvos = []
    for arquivo in arquivos:
        if arquivo.content_type not in TIPOS_PERMITIDOS:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Tipo nao permitido em '{arquivo.filename}'. Envie JPEG OU PNG")
        if arquivo.size is not None and arquivo.size > TAMANHO_MAXIMO:
            raise HTTPException(status_code=status.HTTP_413_CONTENT_TOO_LARGE, detail=f"Arquivo '{arquivo.filename}' muito grande (max 5 MB)")
        if arquivo.filename is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Arquivo sem nome")
        nome = Path(arquivo.filename).name
        with open(PASTA_UPLOAD/nome, "wb") as buffer:
            shutil.copyfileobj(arquivo.file, buffer)
        salvos.append(nome)
    return{"salvos": salvos, "total": len(salvos)}

