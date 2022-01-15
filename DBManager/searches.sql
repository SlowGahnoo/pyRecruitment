-- Count available jobs
/*
SELECT COUNT(*) as available_jobs
FROM REQUEST;
*/

-- Count candidates all, without job, with job
/*
SELECT COUNT(ALL) as all_candidates, COUNT(id_work_pos) as candidates_with_job, COUNT(ALL) - COUNT(id_work_pos) as candidates_with_job
FROM REQUEST AS R LEFT JOIN CANDIDATE AS C ON R.id_candidate=C.id;
*/

-- Αναλυτικά στοιχεία CANDIDATE
/*
SELECT C.id,name,surname,sex,birthday,email,phone_num,street,street_num,zip_code,id_work_pos
FROM CANDIDATE AS C LEFT JOIN USERS AS U ON U.id=C.id;
*/

-- Αναλυτικά στοιχεία αντιπροσώπων
/*
SELECT O.id,name,surname,phone_num,email
FROM OFFICE_REPRESENTATIVE AS O LEFT JOIN USERS AS U ON O.id=U.id;
*/

-- Αναλυτικά στοιχεία εργοδοτών
/*
SELECT E.id,U.name,surname,phone_num,email, C.name as company_name
FROM EMPLOYER AS E LEFT JOIN USERS AS U ON E.id=U.id
				   LEFT JOIN COMPANY AS C ON E.id_company=C.id;
*/

-- Αναλυτικό REQUEST
/*
SELECT C.id,name,surname,sex,birthday,email,phone_num,application_date,desired_wage,job_type,telework,work_experience,degree,foreign_langs,computer_skills,misc_skills
FROM REQUEST AS R LEFT JOIN CANDIDATE AS C ON R.id_candidate=C.id
				  LEFT JOIN USERS AS U ON U.id=C.id
				  LEFT JOIN EDUCATION AS E ON E.id_candidate=C.id;
*/

-- Ομαδοποίηση υποψηφιών ανά τομέα
/*
SELECT S.id,S.name,id_candidate,U.name,surname
FROM SPECIALTY AS S JOIN CANDIDATE_SPECIALTY ON id_specialty=S.id
					JOIN CANDIDATE AS C ON id_candidate=C.id
					JOIN USERS AS U ON U.id=C.id
ORDER BY S.id ASC, id_candidate ASC;
*/

-- Remote jobs
/*
SELECT W.id,S.name as domain, description, telework, total_workers, C.name as company_name
FROM WORK_POSITION AS W  LEFT JOIN SPECIALTY AS S ON W.id_specialty=S.id
						 LEFT JOIN EMPLOYER_WORK_POSITION AS EWP ON W.id=EWP.id_work_position
						 LEFT JOIN EMPLOYER AS  E ON EWP.id_employer=E.id
						 LEFT JOIN COMPANY AS C ON C.id=E.id_company
WHERE telework==1;
*/

-- Non remote jobs
/*
SELECT W.id,S.name as domain, description, telework, total_workers, C.name as company_name
FROM WORK_POSITION AS W  LEFT JOIN SPECIALTY AS S ON W.id_specialty=S.id
						 LEFT JOIN EMPLOYER_WORK_POSITION AS EWP ON W.id=EWP.id_work_position
						 LEFT JOIN EMPLOYER AS  E ON EWP.id_employer=E.id
						 LEFT JOIN COMPANY AS C ON C.id=E.id_company
WHERE telework==0;
*/

-- Universities
/* SELECT name,institute */
/* FROM UNIVERSITY; */
