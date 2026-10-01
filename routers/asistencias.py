from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import Annotated
from models.asistencias import AsistenciaCreate, AsistenciaDB, AsistenciaResponse
from models.usuarios import UserDB
from routers.deps.db_session import SessionDep
from core.dependencies import validate_rol, validate_admin_rol

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
    db_asistencia = AsistenciaDB.model_validate(asistencia)
    db_asistencia.registrado_por = control.nombre
    session.add(db_asistencia)
    session.commit()
    session.refresh(db_asistencia)
    return db_asistencia

