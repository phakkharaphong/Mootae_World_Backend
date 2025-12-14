from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.adapters.db_adapter import get_database_url

DATABASE_URL = get_database_url()

engine = create_engine(DATABASE_URL, echo=True, future=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
