from datetime import date
from sqlmodel import SQLModel, Field, Relationship


class AsistenciaDB(SQLModel, table=True): #molde para tareas
    id: int | None = Field(default=None, primary_key=True)
    fecha: date
    asistencia: str = Field(default="PRESENTE") #por defecto la asistencia es "PRESENTE"
    tutor_id: int = Field(foreign_key="userdb.id") #clave foranea a la tabla de usuarios
    alumno: str
    legajo: int 
    tema: str


class AsistenciaCreate(SQLModel): #modelo de envío desde el front
    fecha:date
    asistencia: str = Field(default="PRESENTE")

# PENDIENTE: Agregar relaciones entre tablas.