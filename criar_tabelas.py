from database import Base, engine
import models.aluno

Base.metadata.create_all(bind=engine) # <- olha todos os models que herdam de Base