from sqlalchemy import create_engine
import os
import sys
import logging

from orm import Base

TIKToK_SOURCE = "tiktok"

def create_db_engine(echo : bool = False):
    db_conn = os.getenv("DATABASE_CONNECTION")
    if db_conn is None:
        print("[WRN] No DATABASE_CONNECTION key from .env found, using default in-memory db",
                file=sys.stderr)
        db_conn = "sqlite+pysqlite:///:memory:"
    
    engine = create_engine(db_conn, echo=echo)

    Base.metadata.create_all(engine)

    return engine

def setup_logging(log_level=logging.DEBUG):
    fmt = "[%(levelname)s] %(asctime)s - %(message)s"
    logging.basicConfig(level=log_level, format=fmt)