from database import Base, engine
from models.aluno import Aluno
from models.curso import Curso

Base.metadata.create_all(bind=engine) # <- olha todos os models que herdam de Base