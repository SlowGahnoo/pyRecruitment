import sqlite3
import os
from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum

dirname = os.path.dirname(__file__)

@dataclass
class Request:
    _id:              int  = 0
    application_date: date = None
    desired_wage:     int  = 0
    job_type:         str  = None

@dataclass 
class Login:
    _id:     int = 0
    email:   str = None
    usrname: str = None
    passwd:  str = None

    def __iter__(self):
        return iter((self._id, self.email, self.usrname, self.passwd))

@dataclass 
class Request:
    _id:               int = 0
    application_date:  date = None
    desired_wage:      str  = None
    job_type:          str  = None
    telework:          int  = 0 # boolean
    work_experience:   int  = 0
    id_candidate:      int  = 0
    id_representative: int  = 0

    def __iter__(self):
        return iter(( _id, application_date,  desired_wage, job_type, telework, work_experience, id_candidate, id_representative))

@dataclass
class Candidate:
    _id:          int  = 0
    name:         str  = None
    surname:      str  = None
    sex:          str  = None
    birthday:     date = None 
    email:        str  = None
    phone_num:    str  = None
    street:       str  = None
    street_num:   int  = 0
    zipcode:      str  = None
    id_work_pos:  int  = 0

    def __iter__(self):
        return iter((self._id, self.name, self.surname, self.sex, self.birthday, self.email, self.phone_num, self.street, self.street_num, self.zipcode))

@dataclass
class Employer:
    _id:          int  = 0
    name:         str  = None
    surname:      str  = None
    email:        str  = None
    phone_num:    str  = None
    company_name: str  = None
    id_company:   int  = 0

    def __iter__(self):
        return iter((self._id, self.name, self.surname, self.email, self.phone_num, self.company_name, id_company))

@dataclass
class Education:
    grade:         int = 0
    ed_start:     date = None
    ed_end:       date = None
    degree:       list = None
    foreign_langs: int = 0
    misc_skills:   str = None
    university:    str = None
    department:    str = None
    def __iter__(self):
        return iter((self.grade, self.ed_start, self.ed_end, self.degree, self.foreign_langs, self.misc_skills, self.university, self.department))

@dataclass
class Job:
    _id:                 int  = 0
    domain:              str  = None
    description:         str  = None
    location:            str  = None
    telework:            int  = 0
    total_workers:       int  = 1
    company_name:        str  = None
    submission_deadline: date = None
    salary:              int  = 0
    id_employer:         int  = 0

@dataclass
class Company:
    _id:       int = 0
    name:      str = None
    est_date: date = 0
    location:  str = None

@dataclass
class OfficeWorker:
    _id:         int = 0
    name:        str = None
    surname:     str = None
    phone_num:   str = None
    email:       str = None
    
class DBManagement:
    def __init__(self, database: str):
        self.con = sqlite3.connect(os.path.join(dirname, database))
        self.cur = self.con.cursor()
        self.cur.executescript(open(os.path.join(dirname, "create.sql")).read())

    def initializeData(self):
        raise NotImplementedError
    
    def getUniversities(self) -> list[str]:
        uni = [str(institute[0]) for institute in self.cur.execute(
        """ SELECT DISTINCT institute FROM UNIVERSITY ORDER BY institute; """).fetchall()]
        return uni

    def getDepartment(self, university: str) -> list[str]:
        dpt = [str(department[0]) for department in self.cur.execute(
        """ SELECT name FROM UNIVERSITY WHERE institute=?""" , (university, )).fetchall()]
        return dpt

    # Login credentials
    def loginUser(self, username, password) -> int:
        _id = [i[0] for i in self.cur.execute(
        """ SELECT id_user FROM LOGIN WHERE username=? AND password=?""", (username, password)
        ).fetchall()]
        return _id[0] if _id else None

    # Register user
    def pushLogin(self, login: Login):
        self.cur.execute("""
            INSERT INTO LOGIN (id_user, email, username, password) VALUES (?, ?, ?, ?)
        """, [*login])

    # Candidate
    def pushCandidate(self, c: Candidate):
        self.cur.execute("""
            INSERT INTO CANDIDATE (id, sex, birthday, zip_code, street, street_num)
            VALUES (?, ?, ?, ?, ?, ?)
        """, [c._id, c.sex, c.birthday, c.zipcode, c.street, c.street_num])

        self.cur.execute("""
            INSERT INTO USERS (id, name, surname, phone_num, email)
            VALUES (?, ?, ?, ?, ?)
        """, [c._id, c.name, c.surname, c.phone_num, c.email])

    def fetchCandidate(self, _id) -> Candidate:
        a = self.cur.execute("""
            SELECT C.id,name,surname,sex,birthday,email,phone_num,street,street_num,zip_code
            FROM CANDIDATE AS C LEFT JOIN USERS AS U ON U.id=C.id
            WHERE U.id=?
        """, (_id, )).fetchall()[0]
        return Candidate(*a)

    def fetchOfficeWorker(self, _id) -> OfficeWorker:
        a = self.cur.execute("""
            SELECT O.id,name,surname,phone_num,email
            FROM OFFICE_REPRESENTATIVE AS O LEFT JOIN USERS AS U ON O.id=U.id
            WHERE U.id=?
        """, (_id, )).fetchall()[0]
        return OfficeWorker(*a)

    def fetchOfficeEmployerIDs(self, _id) -> list[int]:
        ids = [n[0] for n in self.cur.execute("""
            SELECT DISTINCT id_employer FROM OFFICE_REPRESENTATIVE as O LEFT JOIN EMPLOYER_OFFICE_REPRESENTATIVE as ER ON O.id=ER.id_office_representative
            WHERE O.id=?
        """, (_id, ))]
        return ids

    def fetchOfficeRequests(self, _id) -> list[Request]:
        requests = [Request(*a) for a in self.cur.execute("""
            SELECT * FROM REQUEST
            WHERE id_representative=?
        """, (_id, ))]
        return requests

    def pushOfficeWorker(self, o: OfficeWorker):
        self.cur.execute("""
            INSERT INTO OFFICE_REPRESENTATIVE (id)
            VALUES (?)
        """, (o._id, ))

        self.cur.execute("""
            INSERT INTO USERS (id, name, surname, phone_num, email)
            VALUES (?, ?, ?, ?, ?)
        """, [o._id, o.name, o.surname, o.phone_num, o.email])

    def matchCandidateJob(self, id_candidate, id_job):
        self.cur.execute("""
            UPDATE CANDIDATE
            SET id_work_pos=?
            WHERE id=?
        """, (id_job, id_candidate))

    def pushEmployer(self, e: Employer):
        self.cur.execute("""
            INSERT INTO EMPLOYER (id, id_company) 
            VALUES (?, ?)
        """, (e._id, e.id_company))

        self.cur.execute("""
            INSERT INTO USERS (id, name, surname, phone_num, email)
            VALUES (?, ?, ?, ?, ?)
        """, [e._id, e.name, e.surname, e.phone_num, e.email])

    def fetchEmployer(self, _id) -> Employer:
        a = self.cur.execute("""
            SELECT E.id,U.name,surname,phone_num,email, C.name as company_name
            FROM EMPLOYER AS E LEFT JOIN USERS AS U ON E.id=U.id
            				   LEFT JOIN COMPANY AS C ON E.id_company=C.id
            WHERE U.id=?
         """, (_id, )).fetchall()[0]

        return Employer(*a)
    
    def pushCompany(self, c: Company):
        self.cur.execute("""
            INSERT OR IGNORE INTO COMPANY (id, name, location, est_date) 
            VALUES (?, ?, ?, ?)
        """, (c._id, c.name, c.location, c.est_date))

    def updateCandidate(self, c: Candidate):
        self.cur.execute("""
            UPDATE USERS
            SET name=?, surname=?, phone_num=?
            WHERE id=?
        """, (c.name, c.surname, c.phone_num, c._id))

        self.cur.execute("""
            UPDATE CANDIDATE
            SET sex=?, street=?, street_num=?, zip_code=?
            WHERE id=?
        """, (c.sex, c.street, c.street_num, c.zipcode, c._id))

    def deleteCandidate(self):
        raise NotImplementedError

    # Requests
    def pushRequest(self, r: Request):
        print("Pushing request ", r)
        self.cur.execute("""
            INSERT INTO REQUEST (application_date, desired_wage, job_type, telework, work_experience, id_candidate, id_representative)
            VALUES (?, ?, ?, ?, ?, ? ,?)
                """, (r.application_date, r.desired_wage, r.job_type, r.telework, r.work_experience, r.id_candidate, 24))

    def fetchRequest(self, _id) -> Request:
        requests = [Request(*a) for a in self.cur.execute("""
            SELECT R.id, application_date,desired_wage,job_type,telework,work_experience, U.id, R.id_representative
            FROM REQUEST AS R LEFT JOIN CANDIDATE AS C ON R.id_candidate=C.id
            				  LEFT JOIN USERS AS U ON U.id=C.id
            				  LEFT JOIN EDUCATION AS E ON E.id_candidate=C.id
            WHERE U.id=?
                """, (_id, )).fetchall()]
        return requests

    def updateRequest(self):
        raise NotImplementedError

    def deleteRequest(self, r: Request):
        self.cur.execute("""
            DELETE FROM REQUEST
            WHERE id=?
        """, (r._id, ))


    def fetchSpecialties(self):
        specialties = [s[0] for s in self.cur.execute("""
            SELECT name FROM SPECIALTY
        """)]
        return specialties

    # Jobs
    def fetchJob(self, _id) -> list[Job]:
        """ Fetch all available jobs submitted by an Employer """
        jobs = [Job(*a) for a in self.cur.execute("""
            SELECT DISTINCT W.id,S.name as domain, description, W.location, telework, total_workers, C.name as company_name, submission_deadline, salary
            FROM WORK_POSITION AS W  LEFT JOIN SPECIALTY AS S ON W.id_specialty=S.id
            						 LEFT JOIN EMPLOYER_WORK_POSITION AS EWP ON W.id=EWP.id_work_position
            						 LEFT JOIN EMPLOYER AS  E ON EWP.id_employer=E.id
            						 LEFT JOIN COMPANY AS C ON C.id=E.id_company
			WHERE E.id=?
        """, (_id, ))]
        return jobs

    def pushJob(self, j: Job):
        self.cur.execute("""
            INSERT INTO WORK_POSITION (id_specialty, description, location, telework, total_workers) 
            VALUES (?, ?, ?, ?, ?)
        """, (j.domain, j.description, j.location, j.telework, j.total_workers))

        j._id = self.cur.execute("""
            SELECT last_insert_rowid()
        """).fetchall()[0][0]
        print(j._id)

        self.cur.execute("""
            INSERT INTO EMPLOYER_WORK_POSITION (id_work_position, id_employer, submission_deadline, salary) 
            VALUES (?, ?, ?, ?)
        """, (j._id, j.id_employer, j.submission_deadline, j.salary))

    def deleteJob(self):
        raise NotImplementedError

    def commit(self):
        self.con.commit()

    def __str__(self):
        return "\n".join([i[1] for i in self.cur.execute(
            """ SELECT * FROM sqlite_master WHERE type="table" """).fetchall()])

if __name__ == "__main__":
    dbman = DBManagement("test.db")
    print(dbman.fetchOfficeEmployerIDs(24))
    # print(dbman.fetchCandidate(1))
