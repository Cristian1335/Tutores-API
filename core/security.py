from dotenv import load_dotenv
from sqlmodel import Session, select
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
import jwt, os
from datetime import datetime, timedelta, timezone
from models.usuarios import UserDB


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM","")
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

def crear_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

