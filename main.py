#!/usr/bin/env python

from multiprocessing.dummy import Pool as ThreadPool

from argparse import ArgumentParser
from env import create_db_engine, setup_logging
from orm import *
from rapidapi import *
from ripaudio import rip_audio
from transcribe import transcribe
import logging

from sqlalchemy import and_


class TiktokOrchestrator:
    def __init__(self) -> None:
        self.api = RapidApi()

        self.engine = create_db_engine(echo=True)
        
    def run_job(self, job : SSJob, session : Session) -> None:
        if job.job_status in [JobStatus.COMPLETE]:
            job.job_phase = job.job_phase.next_phase()

        job.job_status = JobStatus.RUNNING

        session.commit()
        
        try:
            match job.job_phase:
                case JobPhase.SEARCH:
                    # TODO: need to make proper search functions
                    pass
                
                case JobPhase.DOWNLOAD:
                    job.video_data = self.api.get(job.source)

                case JobPhase.AUDIOSPLIT:
                    job.audio_data = rip_audio(job.video_data)

                case JobPhase.TRANSCRIPTION:
                    job.transcript_data = transcribe(job.audio_data)
                
                case _:
                    # TODO: is it possible to force-exhaustion for a match on enum in Python?
                    pass

        except:
            job.job_status = JobStatus.FAILED
            session.commit()
            raise

        job.job_status = JobStatus.COMPLETE
        session.commit()

    def run_all_jobs(self, until_all_done : bool = False) -> None:
        # TODO: add parallelism


        with Session(self.engine) as session:
            stmt = session.query(SSJob) \
                .where(~and_(SSJob.job_phase == JobPhase.TRANSCRIPTION and SSJob.job_status == JobStatus.COMPLETE), SSJob.job_status != JobStatus.FAILED)

            while stmt.count() > 0:

                jobs = stmt.all()

                for job in jobs:
                    self.run_job(job, session)

                if not until_all_done:
                    break


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-a", "--all", action="store_true", default=False)
    args = parser.parse_args()
    
    load_dotenv()
    setup_logging()

    orch = TiktokOrchestrator()
    orch.run_all_jobs(until_all_done=args.all)