from database import SessionLocal
from models.aluno import Aluno
from models.curso import Curso

session = SessionLocal()

alunos = session.query(Aluno).all()
for a in alunos:
    print(a.id, a.nome, a.idade)

cursos = session.query(Curso).all()
for c in cursos:
    print(c.id, c.nome, c.carga_horaria)

session.close()