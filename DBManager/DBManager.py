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

    def __iter__(self):
        return iter((self._id, self.name, self.surname, self.sex, self.email, self.birthday, self.phone_num, self.street, self.street_num))

@dataclass
class Employer:
    _id:          int  = 0
    name:         str  = None
    surname:      str  = None
    email:        str  = None
    phone_num:    str  = None
    company_name: str  = None

    def __iter__(self):
        return iter((self._id, self.name, self.surname, self.email, self.phone_num, self.company_name))

@dataclass
class Job:
    _id:                 int  = 0
    description:         str  = None
    location:            str  = None
    total_workers:       int  = 1
    submission_deadline: date = None
    salary:              int  = 0
    
class DBManagement:
    def __init__(self, database: str):
        self.con = sqlite3.connect(os.path.join(dirname, database))
        self.cur = self.con.cursor()
        self.cur.executescript(open(os.path.join(dirname, "create.sql")).read())

    def initializeData(self):
        raise NotImplementedError
    
    def getUniversities(self):
        uni = [str(institute[0]) for institute in self.cur.execute(
        """ SELECT DISTINCT institute FROM UNIVERSITY ORDER BY institute; """).fetchall()]
        return uni

    def getDepartment(self, university: str):
        dpt = [str(department[0]) for department in self.cur.execute(
        """ SELECT name FROM UNIVERSITY WHERE institute=?""" , (university, )).fetchall()]
        return dpt

    # Login credentials
    def loginUser(self, username, password):
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

    def fetchCandidate(self, _id):
        a = self.cur.execute("""
            SELECT C.id,name,surname,sex,birthday,email,phone_num,street,street_num,zip_code
            FROM CANDIDATE AS C LEFT JOIN USERS AS U ON U.id=C.id
            WHERE U.id=?
        """, (_id, )).fetchall()[0]
        return Candidate(*a)


    def updateCandidate(self):
        raise NotImplementedError

    def deleteCandidate(self):
        raise NotImplementedError

    # Requests
    def pushRequest(self, r: Request):
        print("Pushing request ", r)
        self.cur.execute("""
            INSERT INTO REQUEST (application_date, desired_wage, job_type, telework, work_experience, id_candidate, id_representative)
            VALUES (?, ?, ?, ?, ?, ? ,?)
                """, (r.application_date, r.desired_wage, r.job_type, r.telework, r.work_experience, r.id_candidate, 24))

    def fetchRequest(self, _id):
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

    def deleteRequest(self):
        raise NotImplementedError

    # Jobs
    def fetchJob(self):
        raise NotImplementedError

    def pushJob(self):
        raise NotImplementedError

    def deleteJob(self):
        raise NotImplementedError

    def commit(self):
        self.con.commit()

    def __str__(self):
        return "\n".join([i[1] for i in self.cur.execute(
            """ SELECT * FROM sqlite_master WHERE type="table" """).fetchall()])

if __name__ == "__main__":
    dbman = DBManagement("test.db")
    print(dbman.fetchRequest(97115100102))
    # print(dbman.fetchCandidate(1))
