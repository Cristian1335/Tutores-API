from sqlmodel import SQLModel, Field
from datetime import date

class TareaBase(SQLModel): #molde para tareas
    nombre: str
    descripcion: str | None = None
    fecha_inicio: date 
    fecha_fin: date | None = None
    estado: str = "PENDIENTE"

class Tarea(TareaBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    tutor_id: int = Field(default=None, foreign_key="userdb.id") #clave foranea a la tabla de tutores

class TareaResponse(TareaBase):
    id: int 
    tutor_id: int | None = None

class TareaCreate(TareaBase):
    tutor_id: int | None = None

class TareaUpdate(SQLModel):
    nombre: str | None = None
    descripcion: str | None = None
    fecha_inicio: date | None = None
    fecha_fin: date | None = None
    tutor_id: int | None = None


