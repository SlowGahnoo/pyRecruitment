CREATE TABLE IF NOT EXISTS WORK_POSITION(
	id            INTEGER	NOT NULL,
	id_specialty  INTEGER	NOT NULL,
	description   TEXT,
	location      TEXT		NOT NULL,
	telework      INTEGER	NOT NULL,
	total_workers INTEGER	DEFAULT 1	NOT NULL,
	PRIMARY KEY(id),
	FOREIGN KEY(id_specialty) REFERENCES SPECIALTY(id),
	CONSTRAINT WORKERS_NOT_NEGATIVE CHECK(total_workers>0),
	CONSTRAINT BOOL_TELEWORK CHECK(telework==true OR telework==false)
);

CREATE TABLE IF NOT EXISTS CANDIDATE(
	id           INTEGER,
	name         TEXT	NOT NULL,
	sex          TEXT	NOT NULL,
	email        TEXT	NOT NULL,
	birthday     DATE	NOT NULL,
	phone        TEXT,
	mobile_phone TEXT	NOT NULL,
	zip_code     INTEGER	NOT NULL,
	street       TEXT	NOT NULL,
	street_num   INTEGER	NOT NULL,
	id_work_pos  INTEGER,
	PRIMARY KEY(id),
	FOREIGN KEY(id_work_pos) REFERENCES WORK_POSITION(id),
	CONSTRAINT EMP_SEX CHECK(sex IN ('M','F'))
);

CREATE TABLE IF NOT EXISTS REQUEST(
	id                INTEGER	NOT NULL,
	application_date  DATE		NOT NULL,
	desired_wage      INTEGER,
	job_type          TEXT		NOT NULL,
	telework          INTEGER,
	work_experience   TEXT,
	id_candidate      INTEGER,
	id_representative INTEGER,
	PRIMARY KEY(id),
	FOREIGN KEY(id_candidate) REFERENCES CANDIDATE(id),
	FOREIGN KEY(id_representative) REFERENCES OFFICE_REPRESENTATIVE(id),
	CONSTRAINT JOB_TYPE CHECK(job_type IN ("FULL","PART")),
	CONSTRAINT TELEWORK_ONLY CHECK(telework==true OR telework==false)
);

CREATE TABLE IF NOT EXISTS EDUCATION(
	degree          TEXT,
	foreign_langs   TEXT,
	computer_skills TEXT,
	misc_skills     TEXT,
	id_candidate    INTEGER,
	FOREIGN KEY(id_candidate) REFERENCES CANDIDATE(id)
);

CREATE TABLE IF NOT EXISTS UNIVERSITY(
	id   INTEGER,
	name TEXT,
	institute TEXT,
	PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS EDUCATION_UNIVERSITY(
	semesters     INTEGER,
	ed_start      DATE,
	ed_end        DATE,
	grade         INTEGER,
	id_candidate  INTEGER,
	id_university INTEGER,
	FOREIGN KEY(id_candidate) REFERENCES EDUCATION(id_candidate),
	FOREIGN KEY(id_university) REFERENCES UNIVERSITY(id)
);

CREATE TABLE IF NOT EXISTS CANDIDATE_SPECIALTY(
	id_candidate INTEGER,
	id_specialty INTEGER,
	FOREIGN KEY(id_candidate) REFERENCES CANDIDATE(id),
	FOREIGN KEY(id_specialty) REFERENCES SPECIALTY(id)
);

CREATE TABLE IF NOT EXISTS CANDIDATE_COMPANY(
	empl_date            DATE,
	leave_date           DATE,
	work_duration        INTEGER,
	position_title       TEXT,
	position_description TEXT,
	id_company           INTEGER,
	id_candidate         INTEGER,
	FOREIGN KEY(id_company) 	REFERENCES COMPANY(id),
	FOREIGN KEY(id_candidate) 	REFERENCES CANDIDATE(id)
);

CREATE TABLE IF NOT EXISTS SPECIALTY(
	id   INTEGER	NOT NULL,
	name TEXT		NOT NULL,
	PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS EMPLOYER_WORK_POSISION(
	id_work_position    INTEGER,
	id_employer         INTEGER,
	submission_deadline DATE,
	salary              INTEGER,
	FOREIGN KEY	(id_work_position) 	REFERENCES WORK_POSITION(id),
	FOREIGN KEY	(id_employer)		REFERENCES EMPLOYER(id)
);

CREATE TABLE IF NOT EXISTS OFFICE_REPRESENTATIVE(
	id			INTEGER	NOT NULL,
	name      	TEXT	NOT NULL,
	surname   	TEXT	NOT NULL,
	sex       	TEXT	NOT NULL,
	phone_num 	TEXT	NOT NULL,
	mail      	TEXT	NOT NULL,
	salary    	INTEGER	NOT NULL,
	hiredate  	DATE	NOT NULL,
	PRIMARY KEY(id),
	CONSTRAINT REPR_SEX CHECK(sex IN ('M','F')),
	CONSTRAINT REPR_SALARY CHECK(salary>0)
);

CREATE TABLE IF NOT EXISTS COMPANY(
	id       INTEGER	NOT NULL,
	name     TEXT		NOT NULL,
	location TEXT		NOT NULL,
	est_date DATE,
	PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS EMPLOYER(
	id         INTEGER	NOT NULL,
	id_company INTEGER,
	name       TEXT		NOT NULL,
	sex        TEXT		NOT NULL,
	surname    TEXT		NOT NULL,
	mail       TEXT		NOT NULL,
	phone_num  TEXT		NOT NULL,
	PRIMARY KEY(id)
	FOREIGN KEY	(id_company) 	REFERENCES COMPANY(id),
	CONSTRAINT 	EMP_SEX 		CHECK(sex IN ('M','F'))
);

CREATE TABLE IF NOT EXISTS EMPLOYER_OFFICE_REPRESENTATIVE(
	id_employer              INTEGER,
	id_office_representative INTEGER,
	FOREIGN KEY(id_employer) 				REFERENCES EMPLOYER(id),
	FOREIGN KEY(id_office_representative) 	REFERENCES OFFICE_REPRESENTATIVE(id)
);

CREATE TABLE IF NOT EXISTS COMPANY_OFFICE_REPRESENTATIVE(
	id_company               INTEGER,
	id_office_representative INTEGER,
	total_cost               INTEGER,
	debit_date               DATE,
	FOREIGN KEY(id_company) 				REFERENCES COMPANY(id),
	FOREIGN KEY(id_office_representative) 	REFERENCES OFFICE_REPRESENTATIVE(id)
);
