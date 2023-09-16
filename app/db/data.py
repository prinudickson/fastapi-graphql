from app.db.database import Base
from app.db.models import Employer, Job, User, JobApplication
from app.auth.hash import hash_password

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

users_data = [
    {"username": "andybek", "password": "ab1234", "email": "hey@andybek.com", "role": "admin"},
    {"username": "user", "password": "user1234", "email": "user@user.com", "role": "user"},
    {"username": "admin", "password": "admin1234", "email": "admin@admin.com", "role": "admin"},
]

job_application_data = [
    {"user_id": 1, "job_id": 1},
    {"user_id": 1, "job_id": 2},
    {"user_id": 2, "job_id": 3}
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

    for user in users_data:
        user['password_hash'] = hash_password(user['password'])
        del user['password']
        u = User(**user)
        session.add(u)

    for jad in job_application_data:
        ja = JobApplication(**jad)
        session.add(ja)


    session.commit()
    session.close()