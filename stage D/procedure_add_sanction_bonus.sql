DECLARE
    v_record_id INT; -- המזהה שיתקבל מה-INSERT
    v_sanction_or_bonus_type CHAR(1);
    v_employee_exists BOOLEAN;
    v_employee_data employee%ROWTYPE; -- רשומה לשליפת נתוני עובד
    v_inserted_record_id INT; -- משתנה שיחזיק את ה-ID שנוצר אוטומטית
BEGIN
    -- 1. טיפול בחריגות עבור כל הפרוצדורה
    BEGIN
        -- 2. וודא שהעובד קיים
        SELECT EXISTS(SELECT 1 FROM employee WHERE employeeid_ = p_emp_id) INTO v_employee_exists;

        IF NOT v_employee_exists THEN
            RAISE EXCEPTION 'Employee with ID % does not exist.', p_emp_id;
        END IF;

        -- אופציונלי: שליפת נתוני העובד לרשומה (שימוש ב-RECORD)
        SELECT * INTO v_employee_data FROM employee WHERE employeeid_ = p_emp_id;

        -- 3. הגדרת סוג הסנקציה/בונוס (שימוש בהסתעפות)
        IF p_is_bonus THEN
            v_sanction_or_bonus_type := 'B';
            IF p_amount <= 0 THEN
                RAISE EXCEPTION 'Bonus amount must be positive.';
            END IF;
        ELSE
            v_sanction_or_bonus_type := 'S';
            IF p_amount <= 0 THEN
                RAISE EXCEPTION 'Sanction amount must be positive.';
            END IF;
        END IF;

        -- 4. הכנסת רשומה לטבלת sanctionbonus
        -- שימו לב: הוספנו את dategiven והגדרנו אותו ל-CURRENT_DATE
        INSERT INTO sanctionbonus (sanction_or_bonus_, amount_, reason, dategiven)
        VALUES (v_sanction_or_bonus_type, p_amount, p_reason, CURRENT_DATE) -- כאן הוספנו את dategiven
        RETURNING recordid_ INTO v_inserted_record_id; -- שליפת ה-ID שנוצר אוטומטית

        -- 5. הכנסת רשומה לטבלת has_sanctionreward
        INSERT INTO has_sanctionreward (recordid_, employeeid_, date_)
        VALUES (v_inserted_record_id, p_emp_id, CURRENT_DATE);

        -- 6. אופציונלי: עדכון הסכום הכולל בטבלת העובד
        -- (ודא שהעמודה 'total_bonus_sanction_amount' קיימת בטבלת employee)
        IF p_is_bonus THEN
            UPDATE employee
            SET total_bonus_sanction_amount = COALESCE(total_bonus_sanction_amount, 0) + p_amount
            WHERE employeeid_ = p_emp_id;
        ELSE -- זו סנקציה
            UPDATE employee
            SET total_bonus_sanction_amount = COALESCE(total_bonus_sanction_amount, 0) - p_amount
            WHERE employeeid_ = p_emp_id;
        END IF;

        RAISE NOTICE 'Successfully added % of type % for employee %.', p_amount, v_sanction_or_bonus_type, p_emp_id;

    EXCEPTION
        -- טיפול בשגיאת "Unique violation" (אם recordid_ הוא PRIMARY KEY ומוכנס ידנית, או דאבל INSERT)
        WHEN unique_violation THEN
            RAISE EXCEPTION 'A unique constraint violation occurred: %', SQLERRM;
        -- טיפול בשגיאת "Foreign Key violation" (אם employeeid_ לא קיים בטבלת employee)
        WHEN foreign_key_violation THEN
            RAISE EXCEPTION 'Foreign key violation: Employee ID % does not exist or related record is missing.', p_emp_id;
        -- טיפול בכל שגיאה אחרת
        WHEN OTHERS THEN
            RAISE EXCEPTION 'An unexpected error occurred in add_sanction_bonus for employee %: %', p_emp_id, SQLERRM;
    END; -- סיום בלוק ה-BEGIN הפנימי
END;

