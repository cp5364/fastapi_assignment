from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, session
# from sqlalchemy.ext.declarative import declarative_base
import logging

from src.utils.config import settings


# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

def get_db() -> session:
    with SessionLocal() as session:
        try:
            yield session
        except Exception as exception:
            logging.error(f"Error retreiving session | {exception}")
            raise Exception(exception)