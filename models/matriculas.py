from sqlalchemy import Table, Column, ForeignKey
from database import Base

matriculas = Table(
    "matriculas",

    Base.metadata,
    
    Column("aluno_id", ForeignKey("alunos.id"), primary_key=True),

    Column("curso_id", ForeignKey("cursos.id"), primary_key=True))