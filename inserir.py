from database import SessionLocal
from models.aluno import Aluno
from models.curso import Curso

session = SessionLocal()

curso_existe = session.get(Curso, 3)
novo_aluno = Aluno(nome="Gabriel", idade=23)
if curso_existe is not None:
    novo_aluno.cursos.append(curso_existe)
session.add(novo_aluno)
session.commit()

print(novo_aluno.id)
session.close()

session = SessionLocal()

novo_curso = Curso(nome="HTML", carga_horaria=360)
session.add(novo_curso)
session.commit()

print(novo_curso.id)
session.close()