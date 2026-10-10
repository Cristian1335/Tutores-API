from sqlmodel import Session, select,col
from models.tareas import Tarea
from datetime import date


def get_tareas(
    session:Session,
    user_id: int,
    skip: int,
    limit: int,
    nombre_tarea: str | None = None,
    fecha: date | None = None,
    estado: str | None = None
    ):
    # filtrado dinamico 
    filtros = [col(Tarea.tutor_id) == user_id]
    if nombre_tarea:
        filtros.append(col(Tarea.nombre).icontains(nombre_tarea))
    if fecha:
        filtros.append(col(Tarea.fecha_inicio) == fecha)
    if estado:
        filtros.append(col(Tarea.estado) == estado)
    
    statement = select(Tarea).where(*filtros).offset(skip).limit(limit)
    tareas_asignadas = session.exec(statement).all()
    return tareas_asignadas

