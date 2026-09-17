from sqlmodel import SQLModel, Field
from pydantic import EmailStr

class UserBase(SQLModel): #molde para usuarios
    username: str #Por convenios de OAuth2, debe tener un username el usuario.
    nombre: str
    apellido: str
    email: EmailStr
    rol: str  = Field(default="TUTOR") #rol por defecto es tutor
    disabled: bool | None = Field(default=False) #por defecto el tutor no está deshabilitado


class UserCreate(UserBase): #modelo de envío desde el front
    password: str

class UserResponse(UserBase): #modelo de respuesta al front
    id: int

class UserUpdate(SQLModel): #modelo de actualización de usuario
    username: str | None = None
    nombre: str | None = None
    apellido: str | None = None
    email: EmailStr | None = None
    disabled: bool | None = None

class UserDB(UserBase, table=True): #Tabla de usuarios en la base de datos
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str


