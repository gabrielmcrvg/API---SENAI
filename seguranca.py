from pwdlib import PasswordHash

pwd_hash = PasswordHash.recommended()

def gerar_hash(senha: str) -> str:
    return pwd_hash.hash(senha)

def verificar_senha(senha, hash_senha) -> bool:
    return pwd_hash.verify(senha, hash_senha)
