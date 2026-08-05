from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

URL_BANCO = 'sqlite:///escola.db'
engine = create_engine(URL_BANCO, connect_args={'check_same_thread': False}) # <- conexão com o BD
SessionLocal = sessionmaker(bind=engine) # <- conversa diretamente e individualmente com o BD

class Base(DeclarativeBase): # <- classe mãe de todos os models
    pass