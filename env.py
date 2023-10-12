from sqlalchemy import create_engine, Column, Integer, String
import os
import sys

from orm import Base

def create_db_engine(echo : bool = False):
    db_conn = os.getenv("DATABASE_CONNECTION")
    if db_conn is None:
        print("[WRN] No DATABASE_CONNECTION key from .env found, using default in-memory db",
                file=sys.stderr)
        db_conn = "sqlite+pysqlite:///:memory:"
    
    engine = create_engine(db_conn, echo=echo)

    Base.metadata.create_all(engine)

    return engine