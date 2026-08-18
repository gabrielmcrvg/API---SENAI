from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
from models.matriculas import matriculas



class Aluno(Base):
    __tablename__ = "alunos"

    id: Mapped[int] = mapped_column(primary_key=True) # PK
    nome: Mapped[str]
    idade: Mapped[int]
    ativo: Mapped[bool] = mapped_column(default=True)
    cursos: Mapped[list["Curso"]]= relationship(secondary=matriculas, back_populates="alunos")