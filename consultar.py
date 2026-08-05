from database import SessionLocal
from models.aluno import Aluno

session = SessionLocal()

alunos = session.query(Aluno).all()
for a in alunos:
    print(a.id, a.nome, a.idade)

session.close()