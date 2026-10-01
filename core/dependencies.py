from typing import Annotated
from fastapi import Depends, HTTPException, status
from .security import SECRET_KEY, ALGORITHM, oaut2scheme
from models.token import TokenData
from models.usuarios import UserDB
from routers.deps.db_session import SessionDep
import jwt
from jwt.exceptions import InvalidTokenError
from sqlmodel import select

async def get_current_user(token: Annotated[str, Depends(oaut2scheme)], session: SessionDep):
    credentials_error = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate user",
        headers={"WWW-Authenticate":"Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_error
        token_data = TokenData(username = username)
    except InvalidTokenError:
        raise credentials_error
    statement =select(UserDB).where(UserDB.email == token_data.username)
    user = session.exec(statement).first()
    if user is None:
        raise credentials_error
    return user

async def get_current_active_user(current_user: Annotated[UserDB, Depends(get_current_user)]):
    if current_user.disabled: 
        raise HTTPException(status_code=400, detail ="Usuario inactivo")
    return current_user

def validate_rol(current_user: UserDB = Depends(get_current_active_user)):
    roles = ["CONTROL","COORDINADOR","ADMIN","SUPER_USER"]
    if current_user.rol not in roles:
        raise HTTPException(
            status_code= status.HTTP_403_FORBIDDEN,
            detail="No tiene los permisos necesarios para acceder",
        )
    return current_user

def validate_admin_rol(current_user: UserDB = Depends(get_current_active_user)):
    roles = ["ADMIN","SUPER_USER"] 
    if current_user.rol not in roles:
        raise HTTPException(
            status_code= status.HTTP_403_FORBIDDEN,
            detail="No tiene los permisos necesarios para acceder"
        )
    return current_user