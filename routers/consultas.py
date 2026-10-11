from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from sqlmodel import select
from models.consultas import RegistroConsultaCreate, RegistroConsultaResponse, RegistroConsultaDB
from routers.deps.db_session import SessionDep
from core.dependencies import validate_admin_rol, validate_rol, get_current_active_user
from models.usuarios import UserDB
from services.estadisticas import obtener_estadisticas_consultas
from services.AI_services import analizar_eficiencia_con_ia

router = APIRouter(
    prefix="/consultas",
    tags=["consultas"]
)

@router.post("/cargar", response_model=RegistroConsultaResponse)
def cargar_consulta(session: SessionDep, consulta: RegistroConsultaCreate, user: Annotated[UserDB, Depends(get_current_active_user)]):
    """Registra una nueva consulta al espacio de consultas."""
    consulta_data = consulta.model_dump()
    db_consulta = RegistroConsultaDB(**consulta_data)
    session.add(db_consulta)
    session.commit()
    session.refresh(db_consulta)
    return db_consulta

@router.get("/", response_model=list[RegistroConsultaResponse])
def get_consultas(session: SessionDep, user: Annotated[UserDB, Depends(validate_admin_rol)], skip: int = 0, limit: int = 50):
    """Lista todas las consultas registradas."""
    statement = select(RegistroConsultaDB).offset(skip).limit(limit)
    consultas = session.exec(statement).all()
    return consultas

@router.get("/estadisticas", response_model=dict)
def get_estadisticas(session: SessionDep, user: Annotated[UserDB, Depends(validate_admin_rol)]):
    """Genera un reporte de eficiencia basado en el volumen de consultas usando IA"""
    #traigo los datos agrupados
    volumen_consultas = obtener_estadisticas_consultas(session)
    
    #envio a la ia para que devuelva un analisis y recomendaciones
    insights_ia = analizar_eficiencia_con_ia(volumen_consultas)
    
    return {
        "datos_historicos_grafico": volumen_consultas,
        "analisis_y_recomendaciones_ia": insights_ia
    }