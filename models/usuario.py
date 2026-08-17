from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    papel: Mapped[str] = mapped_column(default="Comum")