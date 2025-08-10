 # app/core/database.py
import os
from typing import Generator
from dotenv import load_dotenv
from sqlalchemy.ext.declarative import declarative_base
from sqlmodel import create_engine, Session, SQLModel

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

# 1. Reintroduce la clase Base de SQLAlchemy
Base = declarative_base()

def create_db_and_tables():
    # Usa el metadata de SQLModel para crear las tablas
    SQLModel.metadata.create_all(engine)

def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session