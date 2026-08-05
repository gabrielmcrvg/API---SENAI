from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class Aluno(Base):
    __tablename__ = "alunos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str]
    idade: Mapped[int]
    ativo: Mapped[bool] = mapped_column(default=True)