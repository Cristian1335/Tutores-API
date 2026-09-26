from typing import Annotated
from models.usuarios import UserDB, UserCreate, UserResponse, UserUpdate
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import select
from routers.deps.db_session import SessionDep
from core.dependencies import get_current_active_user
from core.security import get_password_hash

not_found_error = HTTPException(status_code=404, detail={"message": "Usuario no encontrado"})

router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"])

@router.post("/", response_model=UserResponse)
def crear_usuario(user: UserCreate, session: SessionDep):
    #verif que no exista ya en la bd 
    verif = session.exec(select(UserDB).where(UserDB.email == user.email)).first()
    if not verif:
        hashed_pwd = get_password_hash(user.password)
        user_dict = user.model_dump(exclude={"password"}) 
        user_dict["hashed_password"] = hashed_pwd #reemplazo texto plano por pwd hasheada
        db_user = UserDB(**user_dict) 

        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user
    else: 
        raise HTTPException(status_code=400, detail={"message": "El usuario existente, inicie sesion"})

#listo los usuarios
@router.get("/", response_model=list[UserResponse])
def get_usuarios(session: SessionDep,
        offset: int = 0, limit: Annotated[int, Query(le=50)] = 50,
        usuario_actual: UserDB = Depends(get_current_active_user) #dep de seguridad para verif de usuario
):
    # Si el código llega a esta línea, es porque el token es válido y el usuario está activo.
    # Puedo usar 'usuario_actual' para saber quién hizo la consulta.
    statement = select(UserDB).offset(offset).limit(limit)
    usuarios = session.exec(statement).all()
    return usuarios

@router.get("/{user_id}", response_model=UserResponse)
def get_usuario(user_id: int, session: SessionDep):
    usuario = session.get(UserDB, user_id)
    if not usuario:
        raise not_found_error
    return usuario

@router.get("/rol/{user_rol}", response_model=list[UserResponse])
def get_coordinadores(user_rol: str, session: SessionDep):
    statement = select(UserDB).where(UserDB.rol == user_rol)
    usuarios = session.exec(statement).all()
    return usuarios

#actualizacion 
@router.patch("/{user_id}", response_model=UserResponse)
def actualizar_usuario(user: UserUpdate, user_id:int, session: SessionDep):
    usuario = session.get(UserDB, user_id)
    if not usuario:
        raise not_found_error
    usuario_info = user.model_dump(exclude_unset= True)
    usuario.sqlmodel_update(usuario_info)
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario




    #clasificacion de la cartografia pregunta de parcial --- Son dos: 
    #    - Tematica
    #    - Base

