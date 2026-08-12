from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session
from typing import Annotated

URL_BANCO = 'sqlite:///escola.db'
engine = create_engine(URL_BANCO, connect_args={'check_same_thread': False}) # <- conexão com o BD

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False) # <- conversa diretamente e individualmente com o BD



def get_db():
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()

SessionDep = Annotated[Session, Depends(get_db)]

class Base(DeclarativeBase): # <- classe mãe de todos os models
    pass