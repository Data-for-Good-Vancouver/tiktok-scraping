import enum

from rapidapi import RapidApi
from sqlalchemy import select, Enum

from sqlalchemy.orm import Mapped, mapped_column, Session
from sqlalchemy.orm import relationship

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, sessionmaker


class JobStatus(enum.Enum):
    RUNNING="running"
    COMPLETE="complete"
    FAILED="failed"

    
class JobPhase(enum.Enum):
    SEARCH="search"
    DOWNLOAD="download"
    AUDIOSPLIT="audio_split"
    TRANSCRIPTION="transcription"


class Base(DeclarativeBase):
    pass


class SSJob(Base):
    __tablename__ = "ss_job"

    id: Mapped[int] = mapped_column(primary_key=True)

    job_status: Mapped[JobStatus]
    job_phase: Mapped[JobPhase]

    tiktok_link: Mapped[str]
    video_data: Mapped[str]
    audio_data: Mapped[str]
    transcript_data: Mapped[str]

    def __init__(self,
                tiktok_link: str,
                job_status: JobStatus = JobStatus.RUNNING,
                job_phase: JobPhase = JobPhase.SEARCH,
                video_data: str = "",
                audio_data: str = "",
                transcript_data: str = ""):
        self.tiktok_link = tiktok_link

        self.job_status = job_status
        self.job_phase = job_phase

        self.video_data = video_data
        self.audio_data = audio_data
        self.transcript_data = transcript_data

    def __repr__(self):
        return f"{self.id} -> {self.tiktok_link}"

    def AdjustPhase(self, new_phase : JobPhase) -> None:
        self.job_phase = new_phase

        
engine = create_engine("sqlite+pysqlite:///db.sql", echo=True)

Base.metadata.create_all(engine)

with Session(engine) as session:
    ssjob1 = SSJob(tiktok_link="tiktok.com/123")
    ssjob2 = SSJob(tiktok_link="tiktok.com/oiuejrw")

    session.add_all([ssjob1, ssjob2])

    session.commit()

    for job in session.scalars(select(SSJob)):
        print(job)