
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from routers.deps.db_session import SessionDep
from core.dependencies import get_current_active_user, validate_admin_rol, validate_rol
from models.usuarios import UserDB
from models.tareas import TareaResponse, Tarea, TareaCreate, TareaUpdate
from sqlmodel import select

router = APIRouter(
    prefix="/tareas",
    tags=["tareas"]
)

@router.get("/", response_model=list[TareaResponse])
def get_tareas(
    session: SessionDep, 
    usuario:Annotated[UserDB,Depends(validate_rol)],
    skip: int = 0, 
    limit: int = 50
):
    """Obtener todas las tareas"""
    statement = select(Tarea).offset(skip).limit(limit)
    tareas = session.exec(statement).all()
    return tareas

@router.get("/{tutor_id}", response_model=list[TareaResponse])
def get_tareas_tutor(
    tutor_id: int, 
    session: SessionDep, 
    usuario: Annotated[UserDB,Depends(validate_rol)],
    skip: int = 0,
    limit: int = 50
):
    """Obtener todas las tareas de un tutor especifico"""
    validate_tutor = session.get(UserDB, tutor_id)
    if not validate_tutor:
        raise HTTPException(status_code=404, detail="Tutor no encontrado")
    statement = select(Tarea).where(Tarea.tutor_id == tutor_id).offset(skip).limit(limit)
    tareas = session.exec(statement).all()
    return tareas

@router.post("/", response_model=TareaResponse,status_code=status.HTTP_201_CREATED)
def create_tarea(
    tarea: TareaCreate, 
    session: SessionDep, 
    usuario: Annotated[UserDB, Depends(validate_rol)]
):
    """Crear una nueva tarea"""
    validate_tutor = session.get(UserDB, tarea.tutor_id)
    if not validate_tutor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"No se puede asignar la tarea. El tutor con ID: {tarea.tutor_id} no existe"
        )
    if (tarea.fecha_fin) and (tarea.fecha_fin < tarea.fecha_inicio):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La fecha de finalización no puede ser anterior a la fecha de inicio"
        )

    data = tarea.model_dump()
    db_tarea = Tarea(**data)
    session.add(db_tarea)
    session.commit()
    session.refresh(db_tarea)
    return db_tarea

@router.delete("/{tarea_id}", response_model=dict)
def delete_tarea(tarea_id: int, session: SessionDep, usuario: Annotated[UserDB, Depends(validate_rol)]):
    """Eliminar una tarea por su ID"""
    tarea = session.get(Tarea, tarea_id)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    session.delete(tarea)
    session.commit()
    return {"message": "Tarea eliminada exitosamente"}

@router.patch("/{tarea_id}", response_model=TareaResponse)
def update_tarea(
    session: SessionDep, 
    tarea_id: int, 
    tarea: TareaUpdate, 
    usuario: Annotated[UserDB, Depends(get_current_active_user)]
):
    """Actualizar una tarea por su ID"""
    db_tarea = session.get(Tarea, tarea_id)
    if not db_tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
    update_data = tarea.model_dump(exclude_unset=True)
    for key, value in update_data.items():   #esto lo realiza sqlmodel_update, pero lo hice manualmente para poder comprenderlo
        setattr(db_tarea, key, value)
    
    session.add(db_tarea)
    session.commit()
    session.refresh(db_tarea)
    return db_tarea