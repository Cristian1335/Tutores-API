from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated


from core.security import crear_access_token, authenticate_user
from models.token import Token
from .deps.db_session import SessionDep

router = APIRouter(tags = ["autentificacion"])

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user: 
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate":"Bearer"}
        )
    access_token = crear_access_token(data={"sub": user.email})
    return Token( access_token= access_token, token_type = "bearer")



