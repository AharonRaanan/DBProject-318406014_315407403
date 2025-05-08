-- שינוי שמות טבלאות שמסתיימות ב- '_'

ALTER TABLE public.department_ RENAME TO department;
ALTER TABLE public.employee_ RENAME TO employee;
ALTER TABLE public.employee_shift_ RENAME TO employee_shift;
ALTER TABLE public.position_ RENAME TO position;
ALTER TABLE public.sanctionbonus_ RENAME TO sanctionbonus;
ALTER TABLE public.shift_ RENAME TO shift;

-- הוספה של מחלקת רפואה בישות מחלקה --

INSERT INTO public.department (departmentid_, name_, email)
VALUES (504, 'Medicine', 'medicine@company.com');

-----------------
השאילתא מבצעת: 
א.
 שתרשום לי בעמודה positionid_ מספרים מ 501 עד 1500
ב. 
שב title_ 
היא תעתיק לי את את כל הנתונים בהתאמה שנמצאים בעמודה 'התמחות' בישות doctors
כלומר משורה 501 ועד שורה 1500
ושתוסיף לכל נתון שם את המילה רפואה באנגלית לפני
ג. שתיתן שכר רנדומלי בין 30000 ל 150000
ד.
בעמודה של departmentid_ 
משורה 501
ועד 1500
הנתון יהיה שם 504
-------------------------
WITH doctor_specializations AS (
    SELECT doc_id, specialization
    FROM public.doctors
    ORDER BY doc_id
    LIMIT 1000 OFFSET 0
)
-- הוספת השורות החדשות לטבלת position
INSERT INTO public.position (positionid_, title_, departmentid_, basesalary_)
SELECT
    gs.series,           -- positionid מ-501 ועד 1500 (לא יותר)
    ds.specialization,   -- התמחות לעמודת title_
    504,                 -- departmentid תמיד 504
    (30000 + (RANDOM() * 70000))::double precision  -- שכר אקראי בין 30000 ל-100000
FROM generate_series(501, 1500) AS gs(series)  -- יוצר סדרה מ-501 עד 1500
JOIN doctor_specializations ds ON gs.series - 500 = ds.doc_id;  -- מחבר את doc_id עם positionid


-- העברת נתונים מדוקטור לעובד ------

WITH doctor_hires AS (
    SELECT doc_fname, doc_lname, hiredate, ROW_NUMBER() OVER (ORDER BY doc_id) AS rn
    FROM public.doctors
    LIMIT 1000 OFFSET 0
)


-- הוספת השורות החדשות לטבלת employee
INSERT INTO public.employee (employeeid_, firstname_, lastname_, positionid_, active, hire_date, birthdate_)
SELECT
    gs.series + 1000 AS employeeid_,        -- מתחילים מ-1001 ועד 2000
    dh.doc_fname AS firstname_,             -- ממקם את doc_fname בעמודת firstname_
    dh.doc_lname AS lastname_,              -- ממקם את doc_lname בעמודת lastname_
    gs.series + 500 AS positionid_,         -- מתחילים מ-501 ועד 1500
    true AS active,                          -- מסמן את כל השורות כ-true בעמודת active
    dh.hiredate AS hire_date,                -- ממקם את hiredate לעמודת hire_date
    '1970-01-01'::date AS birthdate_        -- מכניס תאריך זמני לכל השורות
FROM generate_series(1, 1000) AS gs(series) -- יוצר סדרה של מספרים מ-1 עד 1000
JOIN doctor_hires dh ON gs.series = dh.rn; -- מחבר את הגנרטור עם השורות ב-`doctor_hires`

-- עדכון טבלת doctors --------------------------------------

-- שינוי שם העמודה מ- doc_id ל- employeeid_
ALTER TABLE public.doctors
RENAME COLUMN doc_id TO employeeid_;

-- שמירה רק על העמודות הנדרשות
ALTER TABLE public.doctors
DROP COLUMN doc_fname, 
DROP COLUMN doc_lname, 
DROP COLUMN specialization, 
DROP COLUMN hiredate;

-- עדכון העמודה employeeid_ בטווח 1001 עד 2000
WITH doctor_ids AS (
    SELECT employeeid_, ROW_NUMBER() OVER (ORDER BY employeeid_) AS rn
    FROM public.doctors
)

UPDATE public.doctors
SET employeeid_ = 1000 + doctor_ids.rn
FROM doctor_ids
WHERE public.doctors.employeeid_ = doctor_ids.employeeid_;

-- ביטול מפתח זר  -----

ALTER TABLE public.medicalequipmentreceiving
DROP CONSTRAINT medicalequipmentreceiving_doc_recommends_id_fkey;


ALTER TABLE public.medicaltreatments
DROP CONSTRAINT medicaltreatments_new_doc_id_fkey;

ALTER TABLE public.doctors
DROP CONSTRAINT doctors_pkey;

--- עדכון ה id של הטבלאות ------

UPDATE public.medicalequipmentreceiving
SET employeeid_ = employeeid_ + 1000
WHERE employeeid_ IS NOT NULL;

UPDATE public.medicaltreatments
SET doc_id = doc_id + 1000
WHERE doc_id IS NOT NULL;

--- החזרת מפתח זר/עיקרי אחרי עדכון הערכים ------

ALTER TABLE public.doctors
ADD CONSTRAINT doctors_employeeid_fkey FOREIGN KEY (employeeid_)
REFERENCES public.employee(employeeid_);

ALTER TABLE public.doctors
ADD CONSTRAINT doctors_pkey PRIMARY KEY (employeeid_);

ALTER TABLE public.medicalequipmentreceiving
ADD CONSTRAINT medicalequipmentreceiving_doc_recommends_id_fkey FOREIGN KEY (employeeid_)
REFERENCES public.doctors(employeeid_);

ALTER TABLE public.medicaltreatments
ADD CONSTRAINT medicaltreatments_new_doc_id_fkey FOREIGN KEY (doc_id)
REFERENCES public.doctors(employeeid_);


-- שינוי שם העמודה מ- doc_id ל- employeeid_
ALTER TABLE public.medicaltreatments
    RENAME COLUMN doc_id TO employeeid_;








