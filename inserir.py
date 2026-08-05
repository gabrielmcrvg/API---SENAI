from database import SessionLocal
from models.aluno import Aluno

session = SessionLocal()

novo = Aluno(nome="Ana Souza", idade=29)
session.add(novo)
session.commit()

print(novo.id)
session.close()