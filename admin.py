from sqlmodel import Session, select
from models.usuarios import UserDB
from config.db import engine 
from core.security import get_password_hash 
import getpass

def crear_super_usuario():
    print("--- Configuración inicial del Super Usuario ---")
    email_input = input("Ingresá el email para el admin: ")
    password_input = getpass.getpass("Ingresá una contraseña segura: ") 

    with Session(engine) as session:
        admin_existente = session.exec(select(UserDB).where(UserDB.email == email_input)).first()
        
        if admin_existente:
            print("Ese administrador ya existe en la base de datos.")
            return

        nuevo_admin = UserDB(
            username="admin",
            email=email_input,
            nombre="Admin",
            apellido="Principal",
            hashed_password= get_password_hash(password_input), 
            rol="SUPER_USER"
        )
        
        session.add(nuevo_admin)
        session.commit()
        print("¡Administrador creado con éxito! Ya puedes iniciar sesión en /docs.")

if __name__ == "__main__":
    crear_super_usuario()