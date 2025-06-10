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
-----------------------------------------------------------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION calculate_employee_seniority(p_emp_id INT)
RETURNS INT AS $$
DECLARE
    -- שימוש ברשומה (%ROWTYPE) לשליפת נתוני העובד
    v_employee_record employee%ROWTYPE;
    v_years_worked INT;
BEGIN
    -- טיפול בשגיאות ברמה גבוהה יותר עם BEGIN...EXCEPTION
    BEGIN
        -- שליפת נתוני העובד לתוך הרשומה
        SELECT *
        INTO v_employee_record
        FROM employee
        WHERE employeeid_ = p_emp_id;

        -- בדיקה אם העובד קיים (NOT FOUND אחרי SELECT INTO)
        IF NOT FOUND THEN
            RAISE EXCEPTION 'Employee with ID % does not exist.', p_emp_id;
        END IF;

        -- בדיקה אם העובד אינו פעיל
        IF NOT v_employee_record.active THEN -- גישה לשדה דרך הרשומה
            RAISE EXCEPTION 'Employee % is not currently active.', p_emp_id;
        END IF;

        -- בדיקה אם אין תאריך התחלה
        IF v_employee_record.hire_date IS NULL THEN -- גישה לשדה דרך הרשומה
            RAISE EXCEPTION 'Hire date is missing for employee %.', p_emp_id;
        END IF;

        -- חישוב ותק לפי שנים בלבד
        v_years_worked := DATE_PART('year', CURRENT_DATE) - DATE_PART('year', v_employee_record.hire_date);

        -- וודא שהוותק אינו שלילי (למקרה של תאריך עתידי בטעות)
        IF v_years_worked < 0 THEN
            v_years_worked := 0; -- או שניתן לזרוק חריגה אחרת
        END IF;

        RETURN v_years_worked;

    -- בלוק טיפול בחריגות
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            -- זו חריגה פחות ספציפית אבל יכולה לקרות אם SELECT INTO לא מוצא שורה
            -- במקרה שלנו IF NOT FOUND מטפל בזה לפני כן, אבל זה דוגמה
            RAISE EXCEPTION 'No data found for employee ID %.', p_emp_id;
        WHEN OTHERS THEN
            -- תפיסת כל שגיאה אחרת שלא טופלה ספציפית
            RAISE EXCEPTION 'An error occurred while calculating seniority for employee %: %', p_emp_id, SQLERRM;
    END;
END;
$$ LANGUAGE plpgsql;
