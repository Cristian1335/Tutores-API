from config.db import get_session, create_db_and_tables
from fastapi import FastAPI

create_db_and_tables()

app = FastAPI()
