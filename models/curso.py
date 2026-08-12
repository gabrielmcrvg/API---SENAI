from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
from models.matriculas import matriculas

class Curso(Base):
    __tablename__ = "cursos"

    id: Mapped[int] = mapped_column(primary_key=True) # Mapped quer dizer que o dado é mapeado, responsabilidade do BD
    nome: Mapped[str]
    carga_horaria: Mapped[int]
    alunos: Mapped[list["Aluno"]] = relationship(back_populates="cursos") # type: ignore