from typing import Annotated, Generator
from fastapi import Depends
from sqlmodel import Session
from config.db import get_session

SessionDep = Annotated[Session, Depends(get_session)]