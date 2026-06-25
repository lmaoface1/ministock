from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()  # reads your .env file

DATABASE_URL = os.getenv("DATABASE_URL")  # grabs the value from .env

engine = create_engine(DATABASE_URL)  # connects SQLAlchemy to PostgreSQL

SessionLocal = sessionmaker(           # a factory that creates DB sessions
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

Base = declarative_base()  # your models will inherit from this