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
class Candidate:
    _id:          int  = 0
    name:         str  = None
    surname:      str  = None
    sex:          str  = None
    email:        str  = None
    birthday:     date = None 
    phone:        str  = None
    mobile_phone: str  = None
    street:       str  = None
    street_num:   int  = 0

@dataclass
class Job:
    _id:                 int  = 0
    description:         str  = None
    location:            str  = None
    total_workers:       int  = 1
    submission_deadline: date = None
    salary:              int  = 0
    

class Tables(Enum):
    CANDIDATE = "CANDIDATE",
    REQUEST   = "REQUEST",
    EMPLOYER  = "EMPLOYER",
    COMPANY   = "COMPANY",

class DBManagement:
    def __init__(self, database: str):
        self.con = sqlite3.connect(os.path.join(dirname, database))
        self.cur = self.con.cursor()
        self.cur.executescript(open(os.path.join(dirname, "create.sql")).read())

    def initializeData(self):
        raise NotImplementedError

    # Login credentials
    def loginCandidate(self):
        raise NotImplementedError

    def loginEmployer(self):
        raise NotImplementedError

    # Candidate
    def pushCandidate(self):
        raise NotImplementedError

    def updateCandidate(self):
        raise NotImplementedError

    def deleteCandidate(self):
        raise NotImplementedError

    # Requests
    def createRequest(self):
        raise NotImplementedError

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

    def fetchAll(self, table: Enum):
        """Fetch all rows from a table"""
        return [row for row in self.con.execute("SELECT * FROM ?", (table, )).fetchall()]

    def __str__(self):
        return "\n".join([i[1] for i in self.cur.execute(
            """ SELECT * FROM sqlite_master WHERE type="table" """).fetchall()])

if __name__ == "__main__":
    dbman = DBManagement("test.db")
    print(dbman)
    # c = Request(application_date = datetime.now().strftime("%Y-%m-%d"))
    # print(c)
