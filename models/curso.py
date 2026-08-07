from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class Curso(Base):
    __tablename__ = "cursos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str]
    carga_horaria: Mapped[int]
    alunos: Mapped[list["Aluno"]] = relationship(back_populates="curso") # type: ignore