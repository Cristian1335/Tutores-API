from sqlmodel import SQLModel, Field
from datetime import date

class TareaBase(SQLModel): #molde para tareas
    nombre: str
    descripcion: str | None = None
    fecha_inicio: date 
    fecha_fin: date | None = None

class Tarea(TareaBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    tutor_id: int | None = Field(default=None, foreign_key="userdb.id") #clave foranea a la tabla de tutores

class TareaPublic(TareaBase):
    id: int 
    tutor_id: int | None = None

