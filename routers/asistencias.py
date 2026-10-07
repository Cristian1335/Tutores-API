from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import Annotated
from sqlmodel import select, func
from models.asistencias import AsistenciaCreate, AsistenciaDB, AsistenciaResponse
from models.usuarios import UserDB
from routers.deps.db_session import SessionDep
from core.dependencies import validate_rol, validate_admin_rol, get_current_active_user
from services.asistencia_services import contador_inasistencias, total_asistencias

router = APIRouter(
    prefix="/asistencias",
    tags=["asistencias"]
)

@router.post("/cargar", response_model=AsistenciaResponse)
def cargar_asistencia(session: SessionDep, 
                      asistencia: AsistenciaCreate, 
                      control: Annotated[UserDB, Depends(validate_rol)]
):
    """Registra una nueva asistencia, rol CONTROL o superior."""
    #por algun motivo no me guarda el registrado por
    db_asistencia = AsistenciaDB.model_validate(asistencia)
    db_asistencia.registrado_por = control.nombre
    session.add(db_asistencia)
    session.commit()
    session.refresh(db_asistencia)
    return db_asistencia

@router.get("/", response_model=list[AsistenciaResponse])
def get_asistencias(session: SessionDep, 
                    admin: Annotated[UserDB, Depends(validate_rol)], 
                    limit: Annotated[int, Query(le=50)]=50, offset: int = 0    
):
    """"Lista todas las asistencias registradas"""
    statement = select(AsistenciaDB).limit(limit).offset(offset) #tratar de ordenar descendentemente
    asistencias = session.exec(statement).all()
    return asistencias

@router.get("/me", response_model=dict)
def get_me(user: Annotated[UserDB, Depends(get_current_active_user)], 
           session: SessionDep,
            limit: Annotated[int, Query(le=50)]=50, offset: int = 0              
):
    """Lista el total de asistencias registradas para el usuario""" 
    total = total_asistencias(session, user.id) #ignorar error, es porque inicialmente, al crearse la db, el id puede ser None, pero al estar la dependencia de active_user, es imposible que el user.id sea none
    inasistencias = contador_inasistencias(session, user.id)
    registros = session.exec(select(AsistenciaDB).where(AsistenciaDB.tutor_id == user.id).limit(limit).offset(offset)).all()
    if not registros:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="No se encontraron registros de asistencias para este usuario")
    mensaje = {
        "estadisticas":{
            "total_inasistencias": f"{inasistencias}/{total}"
        },
        "registros:": registros}
    return mensaje

@router.get("/{user_id}", response_model=dict)
def get_particular(session: SessionDep, 
                   user_id: int, 
                   admin: Annotated[UserDB, Depends(validate_admin_rol)], 
                   limit: Annotated[int, Query(le=50)]=50, 
                   offset: int = 0
):
    """Lista los registros cargados para un usuario en particular. Facilita el seguimiento de empleados para el superior"""
    total = total_asistencias(session, user_id)
    inasistencias = contador_inasistencias(session, user_id)
    registros = session.exec(select(AsistenciaDB).where(AsistenciaDB.tutor_id == user_id).limit(limit).offset(offset)).all()
    if not registros:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="No se encontraron registros de asistencias para este usuario")
    mensaje = {
        "estadisticas":{
            "total_inasistencias": f"{inasistencias}/{total}"
        },
        "registros:": registros}
    return mensaje
    

