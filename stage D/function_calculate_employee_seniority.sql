CREATE OR REPLACE FUNCTION calculate_employee_seniority(emp_id INT)
RETURNS INT AS $$
DECLARE
    years_worked INT;
    hire_date_ DATE;
    is_active BOOLEAN;
BEGIN
    -- שליפת תאריך התחלה וסטטוס פעילות
    SELECT hire_date, active INTO hire_date_, is_active
    FROM employee
    WHERE employeeid_ = emp_id;

    -- בדיקה אם העובד קיים
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Employee with ID % does not exist.', emp_id;
    END IF;

    -- בדיקה אם העובד אינו פעיל
    IF NOT is_active THEN
        RAISE EXCEPTION 'Employee % is not currently active.', emp_id;
    END IF;

    -- בדיקה אם אין תאריך התחלה
    IF hire_date_ IS NULL THEN
        RAISE EXCEPTION 'Hire date is missing for employee %.', emp_id;
    END IF;

    -- חישוב ותק לפי שנים בלבד (ללא חודשי דיוק)
    years_worked := DATE_PART('year', CURRENT_DATE) - DATE_PART('year', hire_date_);

    RETURN years_worked;
END;
$$ LANGUAGE plpgsql;
