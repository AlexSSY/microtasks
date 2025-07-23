from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


connect_args = {
    "check_same_thread": False
}

engine = create_engine("sqlite:///db.sqlite3", connect_args=connect_args)
SessionLocal = sessionmaker(engine, autoflush=False, autocommit=False)
Base = declarative_base()
