from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
from models.matriculas import matriculas

class Curso(Base):
    __tablename__ = "cursos"

    id: Mapped[int] = mapped_column(primary_key=True) # PK
    nome: Mapped[str]
    carga_horaria: Mapped[int]
    alunos: Mapped[list["Aluno"]]= relationship(secondary=matriculas, back_populates="cursos")
