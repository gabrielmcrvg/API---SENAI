from fastapi import HTTPException, status

def obter_ou_404(session, model, id, nome):
    obj = session.get(model, id)
    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{nome} não encontrado")
    return obj