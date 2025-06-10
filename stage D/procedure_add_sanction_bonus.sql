CREATE OR REPLACE PROCEDURE add_sanction_bonus(emp_id INT, is_bonus BOOLEAN, reason TEXT, amount DOUBLE PRECISION)
LANGUAGE plpgsql
AS $$
DECLARE
    new_recordid INT;
BEGIN
    new_recordid := (SELECT COALESCE(MAX(recordid_), 0) + 1 FROM sanctionbonus);

    INSERT INTO sanctionbonus(recordid_, amount_, reason, sanction_or_bonus_, dategiven)
    VALUES (new_recordid, amount, reason, CASE WHEN is_bonus THEN 'B' ELSE 'S' END, CURRENT_DATE);

    INSERT INTO has_sanctionreward(recordid_, employeeid_, date_)
    VALUES (new_recordid, emp_id, CURRENT_DATE);
END;
$$;
-----------------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE add_sanction_bonus(
    p_emp_id INT,
    p_is_bonus BOOLEAN,
    p_reason TEXT,
    p_amount NUMERIC(10, 2) -- שינוי ל-NUMERIC
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_record_id INT; -- המזהה שיתקבל מה-INSERT
    v_sanction_or_bonus_type CHAR(1);
    v_employee_exists BOOLEAN;
    v_employee_data employee%ROWTYPE; -- רשומה לשליפת נתוני עובד
BEGIN
    -- 1. טיפול בחריגות עבור כל הפרוצדורה
    BEGIN
        -- 2. וודא שהעובד קיים
        SELECT EXISTS(SELECT 1 FROM employee WHERE employeeid_ = p_emp_id) INTO v_employee_exists;

        IF NOT v_employee_exists THEN
            RAISE EXCEPTION 'Employee with ID % does not exist.', p_emp_id;
        END IF;

        -- אופציונלי: שליפת נתוני העובד לרשומה (שימוש ב-RECORD)
        -- (פחות קריטי כאן, אבל מדגים שימוש ב-RECORD)
        SELECT * INTO v_employee_data FROM employee WHERE employeeid_ = p_emp_id;
        -- RAISE NOTICE 'Processing % for employee % (% %)', p_reason, p_emp_id, v_employee_data.firstname_, v_employee_data.lastname_;

        -- 3. הגדרת סוג הסנקציה/בונוס (שימוש בהסתעפות)
        IF p_is_bonus THEN
            v_sanction_or_bonus_type := 'B';
            -- דוגמה למורכבות: ודא שסכום הבונוס חיובי
            IF p_amount <= 0 THEN
                RAISE EXCEPTION 'Bonus amount must be positive.';
            END IF;
        ELSE
            v_sanction_or_bonus_type := 'S';
            -- דוגמה למורכבות: ודא שסכום הסנקציה חיובי (ייצג קנס)
            IF p_amount
