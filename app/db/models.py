from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Employer(Base):
    __tablename__="employers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    contact_email = Column(String)
    industry = Column(String)
    job = relationship("Job", back_populates="employer", lazy="joined")

class Job(Base):
    __tablename__="jobs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    description = Column(String)
    employer_id = Column(Integer, ForeignKey("employers.id"))
    employer = relationship("Employer", back_populates="job", lazy="joined")
    job_application = relationship("JobApplication", back_populates="job", lazy="joined")

class User(Base):
    __tablename__="users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    password = Column(String)
    email = Column(String)
    role = Column(String)
    job_application = relationship("JobApplication", back_populates="user", lazy="joined")

class JobApplication(Base):
    __tablename__="job_applications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="job_application", lazy="joined")
    job_id = Column(Integer, ForeignKey("jobs.id"))
    job = relationship("Job", back_populates="job_application", lazy="joined")
