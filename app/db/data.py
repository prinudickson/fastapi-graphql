from app.db.database import Base
from app.db.models import Employer, Job

employers_data = [
    {"name": "MetaTechA", "contact_email": "contact@company-a.com", "industry": "Tech"},
    {"name": "MoneySoftB", "contact_email": "contact@company-b.com", "industry": "Finance"},
]

jobs_data = [
    {"title": "Software Engineer", "description": "Develop web applications", "employer_id": 1},
    {"title": "Data Analyst", "description": "Analyze data and create reports", "employer_id": 1},
    {"title": "Accountant", "description": "Manage financial records", "employer_id": 2},
    {"title": "Manager", "description": "Manage people who manage records", "employer_id": 2},
]

def prepare_database(Session, engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    session = Session()

    for employer in employers_data:
        emp = Employer(**employer)
        session.add(emp)

    for job in jobs_data:
        jb = Job(**job)
        session.add(jb)  

    session.commit()
    session.close()