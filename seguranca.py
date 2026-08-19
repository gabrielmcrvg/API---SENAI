from typing import Annotated

from fastapi import Depends, HTTPException, status
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
import jwt

import os
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer

from database import SessionDep
from models.usuario import Usuario

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

pwd_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def gerar_hash(senha: str) -> str:
    return pwd_hash.hash(senha)

def verificar_senha(senha: str, hash_senha: str) -> bool:
    return pwd_hash.verify(senha, hash_senha)

def criar_token(dados: dict) -> str:
    payload = dados.copy()
    exp = datetime.now(timezone.utc) + timedelta(minutes=30)
    payload.update({"exp": exp})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def usuario_atual(session: SessionDep, token: str = Depends(oauth2_scheme)) -> Usuario:
    erro = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Nao foi possivel validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY,
                             algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise erro
    except jwt.PyJWTError:
        raise erro
    usuario = session.query(Usuario).filter(
        Usuario.username == username).first()
    if usuario is None:
        raise erro
    return usuario

UsuarioAtual = Annotated[Usuario, Depends(usuario_atual)]

def apenas_admin(usuario: UsuarioAtual) -> Usuario:
    if usuario.papel != "Admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Somente a Diretoria!")
    return usuario

AdminAtual = Annotated[Usuario, Depends(apenas_admin)]