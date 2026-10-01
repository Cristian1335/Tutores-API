from datetime import date
from sqlmodel import SQLModel, Field, Relationship

class AsistenciaBase(SQLModel):
    fecha: date
    asistencia: str = Field(default="PRESENTE") #por defecto la asistencia es "PRESENTE"
    evento: bool = Field(default=False)

    alumno: str | None = None
    legajo: int | None = None 
    tema: str | None = None

class AsistenciaCreate(AsistenciaBase): #modelo de envío desde el front
    tutor_id: int #id del tutor al que se le registra la asistencia

class AsistenciaResponse(AsistenciaBase):
    id: int

class AsistenciaDB(AsistenciaBase, table=True): #molde para asist
    id: int | None = Field(default=None, primary_key=True)
    tutor_id: int = Field(foreign_key="userdb.id") #clave foranea a la tabla de tutores
    registrado_por: str = Field(default = None) #clave foranea a la tabla de usuarios que registran la asistencia



# PENDIENTE: Agregar relaciones entre tablas.