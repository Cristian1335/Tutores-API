from sqlmodel import SQLModel, Field
from datetime import date

class RegistroConsultaBase(SQLModel):
    fecha: date
    alumno: str | None = None
    legajo: int | None = None
    tema: str | None = None

class RegistroConsultaCreate(RegistroConsultaBase):
    tutor_id: int

class RegistroConsultaResponse(RegistroConsultaBase):
    id: int
    tutor_id: int

class RegistroConsultaDB(RegistroConsultaBase, table=True):
    id: int = Field(default=None, primary_key=True)
    tutor_id: int = Field(foreign_key="userdb.id") 