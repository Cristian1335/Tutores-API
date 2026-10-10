from config.db import create_db_and_tables
from fastapi import FastAPI
from routers import usuarios, auth, asistencias, tareas

create_db_and_tables()

app = FastAPI()
app.include_router(usuarios.router)
app.include_router(auth.router)
app.include_router(asistencias.router)
app.include_router(tareas.router)
