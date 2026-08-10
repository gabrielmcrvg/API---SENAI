from database import Base, engine
import models.aluno
import models.curso
import models.matriculas

Base.metadata.create_all(bind=engine) # <- olha todos os models que herdam de Base