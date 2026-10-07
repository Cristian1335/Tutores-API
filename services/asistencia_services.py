#Logica de negocio para el manejo de asistencias.

from sqlmodel import select, func, Session
from models.asistencias import AsistenciaDB 

def contador_inasistencias(session: Session, user_id: int):
    """Cuenta cantidad de inasistencias registradas para un usuario especifico"""
    statement = select(func.count()).select_from(AsistenciaDB).where(
        AsistenciaDB.tutor_id == user_id,
        AsistenciaDB.asistencia == "AUSENTE"
    )
    total_inasistencias = session.exec(statement).one()
    return total_inasistencias

def total_asistencias(session: Session, user_id: int):
    """Cuenta cantidad total de asistencias registradas para un usuario especifico"""
    statement = select(func.count()).select_from(AsistenciaDB).where(
        AsistenciaDB.tutor_id == user_id
    )
    total_asistencias = session.exec(statement).one()
    return total_asistencias


