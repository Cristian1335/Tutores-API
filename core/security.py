#Acá van las encriptaciones de claves, tokens, y todo lo que tenga que ver con seguridad de la API.
from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pwdlib import PasswordHash
import jwt
from jwt.exceptions import InvalidTokenError
from ..models.usuarios import UserDB
from dotenv import load_dotenv
import os
from sqlmodel import Session, select

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))

oaut2scheme = OAuth2PasswordBearer(tokenUrl="token")
password_hash= PasswordHash.recommended()
dmpwd = os.getenv("DUMMY_PWD", "password_de_respaldo")

DUMMY_HASH = password_hash.hash(dmpwd)


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)

def verify_password(password_plano, hashed_password):
    return password_hash.verify(password_plano, hashed_password)

def get_user(session: Session, username: str):
    statement = select(UserDB).where(UserDB.email == username)
    return session.exec(statement).first()

def authenticate_user(session: Session, username: str, password:str):
    user = get_user(session, username)
    if not user:
        verify_password(password, DUMMY_HASH)
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


