from typing import Annotated
from models.usuarios import UserDB, UserCreate, UserResponse, UserUpdate
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import select
from routers.deps.db_session import SessionDep
from core.dependencies import get_current_active_user, validate_admin_rol, validate_rol
from core.security import get_password_hash

not_found_error = HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail={"message": "Usuario no encontrado"})

router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"])

@router.post("/", response_model=UserResponse)
def crear_usuario(user: UserCreate, session: SessionDep, admin: Annotated[UserDB, Depends(validate_admin_rol)]):
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

@router.get("/me", response_model=dict)
def get_me(session: SessionDep, 
           usuario_actual: Annotated[UserDB,Depends(get_current_active_user)]
):
    """ Devuelve la informacion personal, username, email y estadisticas"""
    info = {
        "id": usuario_actual.id,
        "email": usuario_actual.email,
        "nombre": usuario_actual.nombre,
        "apellido": usuario_actual.apellido,
        "rol": usuario_actual.rol
    }
    inasistencias = 0 #falta realizar el calculo
    tareas_asignadas =[] #lista de tareas. Falta implementar
    respuesta = {
        "user": info,
        "estadisticas":{
            "inasistencias": inasistencias
            #podria implementar un registro de candidad de consultas recibidas para mejorar el seguimiento del espacio
        },
        "tareas": tareas_asignadas
    }
    return respuesta

@router.get("/{user_id}", response_model=UserResponse)
def get_usuario(user_id: int, session: SessionDep, admin:Annotated[UserDB, Depends(validate_admin_rol)]):
    usuario = session.get(UserDB, user_id)
    if not usuario:
        raise not_found_error
    return usuario

@router.get("/rol/{user_rol}", response_model=list[UserResponse])
def get_coordinadores(user_rol: str, session: SessionDep, admin: Annotated[UserDB, Depends(validate_admin_rol)]):
    statement = select(UserDB).where(UserDB.rol == user_rol)
    usuarios = session.exec(statement).all()
    return usuarios

#actualizacion 
@router.patch("/{user_id}", response_model=UserResponse)
def actualizar_usuario(user: UserUpdate, user_id:int, session: SessionDep, usuario_actual:Annotated[UserDB,Depends(get_current_active_user)]
):
    #Un usuario normal solo puede modificarse a sí mismo.
    if usuario_actual.id == user_id or usuario_actual.rol in ["ADMIN","SUPER_USER"]:
        usuario = session.get(UserDB, user_id)
        if not usuario:
            raise not_found_error
        usuario_info = user.model_dump(exclude_unset= True)

        #Interceptacion y hasheo de contraseña
        if "password" in usuario_info:
            hashed_password = get_password_hash(usuario_info["password"])
            usuario_info["hashed_password"] = hashed_password
            del usuario_info["password"]
        if "rol" in usuario_info and usuario_actual.rol not in ["ADMIN","SUPER_USER"]:
            del usuario_info["rol"] 

        usuario.sqlmodel_update(usuario_info)
        session.add(usuario)
        session.commit()
        session.refresh(usuario)
        return usuario
    else:
        raise HTTPException(
                    status_code = status.HTTP_403_FORBIDDEN,
                    detail= "No tiene permisos para realizar esta accion"
                )

@router.patch("/baja/{user_id}") #Soft delete - Baja de usuario desactivandolo
def delete_usuario(
    session: SessionDep,
    user_id: int,
    admin: Annotated[UserDB ,Depends(validate_admin_rol)]
):
    user = session.get(UserDB,user_id)
    if not user:
        raise not_found_error
    user.disabled = True
    session.add(user)
    session.commit()
    return {"message":"Tutor dado de baja exitosamente"}



