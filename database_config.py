from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv(dotenv_path=r"C:\\Users\\chuwo\\OneDrive\\เอกสาร\\Desktop\\all_project\\Mootae_World_Backend\\environment\\.database.env")


DB_URL = DB_URL = os.getenv("DB_URL")
print(f"DB iS {DB_URL}")
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False,autoflush=False, bind=engine)

Base = declarative_base()