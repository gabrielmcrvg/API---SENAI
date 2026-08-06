from database import SessionLocal
from models.aluno import Aluno
from models.curso import Curso

session = SessionLocal()

novo_aluno = Aluno(nome="Gabriel", idade=23)
session.add(novo_aluno)
session.commit()

print(novo_aluno.id)
session.close()

session = SessionLocal()

novo_curso = Curso(nome="Engenharia de Software", carga_horaria=3600)
session.add(novo_curso)
session.commit()

print(novo_curso.id)
session.close()