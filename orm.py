#!/usr/bin/env python

from dotenv import load_dotenv
import env
import logging

import enum

from rapidapi import RapidApi
from sqlalchemy import select, Enum

from sqlalchemy.orm import Mapped, mapped_column, Session
from sqlalchemy.orm import relationship

from sqlalchemy.orm import DeclarativeBase

class JobStatus(enum.Enum):
    WAITING="waiting"
    RUNNING="running"
    COMPLETE="complete"
    FAILED="failed"

    
class JobPhase(enum.Enum):
    SEARCH="search"
    DOWNLOAD="download"
    AUDIOSPLIT="audiosplit"
    TRANSCRIPTION="transcription"

    def next_phase(self):
        """ Gets the next enum in the sequence. In case of overflow resets index to first.

        Returns:
            _type_: _description_
        """
        members = list(JobPhase)
        current_phase_idx = members.index(self) 
        next_phase_idx = (current_phase_idx + 1) % len(JobPhase)
        return members[next_phase_idx]

    
class Base(DeclarativeBase):
    pass


class SSJob(Base):
    __tablename__ = "ss_job"

    id: Mapped[int] = mapped_column(primary_key=True)

    job_status: Mapped[JobStatus]
    job_phase: Mapped[JobPhase]

    origin: Mapped[str]
    source: Mapped[str]
    video_data: Mapped[str]
    audio_data: Mapped[str]
    transcript_data: Mapped[str]

    def __init__(self,
                origin: str,
                source: str,
                job_status: JobStatus = JobStatus.WAITING,
                job_phase: JobPhase = JobPhase.SEARCH,
                video_data: str = "",
                audio_data: str = "",
                transcript_data: str = ""):
        self.origin = origin 
        self.source = source

        self.job_status = job_status
        self.job_phase = job_phase

        self.video_data = video_data
        self.audio_data = audio_data
        self.transcript_data = transcript_data

    def __repr__(self):
        return f"{self.id} -> {self.origin} ({self.job_phase} // {self.job_status})"


if __name__ == "__main__":
    load_dotenv()
    env.setup_logging()
    
    tt_link = "https://www.tiktok.com/@freshdailyvancouver/video/7232154653176188165"
    ssjob1 = SSJob(source=tt_link)
    ssjob2 = SSJob(source="tiktok.com/oiuejrw",
                   video_data="data/57fc8a87-df5e-479d-b5e2-79455a6083c0.mp4",
                   job_phase=JobPhase.AUDIOSPLIT)

    engine = env.create_db_engine(echo=True)

    with Session(engine) as session:

        session.add_all([ssjob2])
        session.commit()
        
        for job in session.scalars(select(SSJob)):
            print(job)