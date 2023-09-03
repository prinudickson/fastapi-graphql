from sqlalchemy import create_engine, Column, Integer, String as sqString, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Employer(Base):
    __tablename__="employers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(sqString)
    contact_email = Column(sqString)
    industry = Column(sqString)
    jobs = relationship("Job", back_populates="employer")

class Job(Base):
    __tablename__="jobs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(sqString)
    description = Column(sqString)
    employer_id = Column(Integer, ForeignKey("employers.id"))
    employer = relationship("Employer", back_populates="jobs")