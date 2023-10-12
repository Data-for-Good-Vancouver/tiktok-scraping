#!/usr/bin/env python

from multiprocessing.dummy import Pool as ThreadPool

from env import create_db_engine
from orm import *
from rapidapi import *
from ripaudio import rip_audio
from transcribe import transcribe


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
                    raise NotImplementedError
                
                case JobPhase.DOWNLOAD:
                    job.video_data = self.api.get(job.source)

                case JobPhase.AUDIOSPLIT:
                    job.audio_data = rip_audio(job.video_data)

                case JobPhase.TRANSCRIPTION:
                    job.transcript_data = transcribe(job.audio_data)
                
                case _:
                    # TODO: is it possible to force exhaustion for a match on enum in Python?
                    pass

        except:
            job.job_status = JobStatus.FAILED
            session.commit()
            raise

        job.job_status = JobStatus.COMPLETE
    
        # TODO: this is very inelegant, fix it
        if job.job_phase == JobPhase.TRANSCRIPTION:
            job.job_phase = JobPhase.DONE
            
        session.commit()

    def run_all_jobs(self) -> None:
        # TODO: add parallelism

        with Session(self.engine) as session:

            jobs = session.scalars(select(SSJob).where(SSJob.job_phase != JobPhase.DONE)).all()

            for job in jobs:
                orch.run_job(job, session)


if __name__ == "__main__":
    orch = TiktokOrchestrator()

    orch.run_all_jobs()