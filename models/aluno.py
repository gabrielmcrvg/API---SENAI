from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from database import Base
from models.matriculas import matriculas

class Aluno(Base):
    __tablename__ = "alunos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str]
    idade: Mapped[int]
    ativo: Mapped[bool] = mapped_column(default=True)
    curso_id: Mapped[int] = mapped_column(ForeignKey("cursos.id")) # <- cursos é o nome da tabela, nao da classe
    curso: Mapped["Curso"] = relationship(secondary=matriculas, back_populates="alunos") # type: ignore