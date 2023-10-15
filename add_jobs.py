#!/usr/bin/env python

from dotenv import load_dotenv
import sys
from sqlalchemy import select
from sqlalchemy.orm import Session
from env import create_db_engine
from orm import SSJob

if __name__ == "__main__":
    load_dotenv()
    engine = create_db_engine(echo=True)
    
    with Session(engine) as session:
        for line in sys.stdin:
            tiktok_link = line.strip()

            if len(tiktok_link) == 0:
                continue
            
            if session.query(SSJob).where(SSJob.source == tiktok_link).count() > 0:
                print(f"Link already exists in jobs: {tiktok_link}", file=sys.stderr)
                continue

            new_job = SSJob(source=tiktok_link)

            session.add(new_job)
            session.commit()