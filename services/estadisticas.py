from sqlmodel import select, func, Session,col
from models.consultas import RegistroConsultaDB

def obtener_estadisticas_consultas(session: Session):
    statement = select(
        col(RegistroConsultaDB.fecha),
        func.count(col(RegistroConsultaDB.tema)).label("total")
    ).group_by(col(RegistroConsultaDB.fecha))

    resultados = session.exec(statement).all()

    return {
        str(fecha): total for fecha, total in resultados if fecha
    }
