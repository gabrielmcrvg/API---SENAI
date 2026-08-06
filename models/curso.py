from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class Curso(Base):
    __tablename__ = "cursos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str]
    carga_horaria: Mapped[int]