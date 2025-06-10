CREATE TABLE IF NOT EXISTS sanction_log (
    log_id SERIAL PRIMARY KEY,
    employeeid_ INT,
    recordid_ INT,
    log_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    action_type TEXT
);
--------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION log_sanction_bonus()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO sanction_log(employeeid_, recordid_, action_type)
    VALUES (NEW.employeeid_, NEW.recordid_, 'INSERT');

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_log_sanction_bonus
AFTER INSERT ON has_sanctionreward
FOR EACH ROW EXECUTE FUNCTION log_sanction_bonus();


-------------------------------------------------------------------%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%--------------------------------------------------------
CREATE OR REPLACE FUNCTION log_sanction_bonus()
RETURNS TRIGGER AS $$
DECLARE
    -- נתונים נוספים שנרצה לשלוף מהטבלאות הקשורות
    v_sanction_or_bonus_type CHAR(1);
    v_amount NUMERIC(10, 2);
    v_employee_name VARCHAR(255);
    v_log_description TEXT;
BEGIN
    -- בלוק לטיפול בחריגות בתוך הטריגר.
    -- חשוב: אם הלוגינג נכשל, אנחנו לא רוצים שהפעולה המקורית (INSERT) תיכשל.
    -- לכן נשתמש ב-RAISE WARNING או RAISE NOTICE במקום RAISE EXCEPTION.
    BEGIN
        -- שליפת נתונים נוספים מהטבלאות המקושרות (sanctionbonus ו-employee)
        -- זוהי דוגמה ל-JOIN בתוך פונקציית טריגר
        SELECT sb.sanction_or_bonus_, sb.amount_, (e.firstname_ || ' ' || e.lastname_)
        INTO v_sanction_or_bonus_type, v_amount, v_employee_name
        FROM sanctionbonus sb
        LEFT JOIN employee e ON NEW.employeeid_ = e.employeeid_ -- נניח ש-employeeid_ קיים ב-employee
        WHERE sb.recordid_ = NEW.recordid_;

        -- בניית תיאור מפורט ללוג (שימוש בהסתעפויות ושרשור טקסט)
        IF v_sanction_or_bonus_type = 'B' THEN
            v_log_description := 'Bonus of ' || v_amount || ' for employee ' || COALESCE(v_employee_name, 'Unknown Employee') || '.';
        ELSIF v_sanction_or_bonus_type = 'S' THEN
            v_log_description := 'Sanction of ' || v_amount || ' for employee ' || COALESCE(v_employee_name, 'Unknown Employee') || '.';
        ELSE
            v_log_description := 'Unknown sanction/bonus type for employee ' || COALESCE(v_employee_name, 'Unknown Employee') || '.';
        END IF;

        -- הכנסת רשומה לטבלת הלוג
        -- אם הוספתם עמודות לטבלת sanction_log, עדכנו את רשימת העמודות כאן.
        INSERT INTO sanction_log(employeeid_, recordid_, action_type, sanction_or_bonus_type, amount, employee_name, log_description)
        VALUES (NEW.employeeid_, NEW.recordid_, TG_OP, v_sanction_or_bonus_type, v_amount, v_employee_name, v_log_description);

    EXCEPTION
        WHEN OTHERS THEN
            -- אם משהו נכשל בלוגינג, נרשום אזהרה ולא נשבור את ה-INSERT המקורי
            RAISE WARNING 'Failed to log sanction/bonus for employee ID % (record ID %). Error: %',
                          NEW.employeeid_, NEW.recordid_, SQLERRM;
            -- לא נזרק EXCEPTION כאן, כדי שהפעולה המקורית בטבלה תצליח
    END;

    -- RETURN NEW חובה לטריגר FOR EACH ROW
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- הגדרת הטריגר
CREATE TRIGGER trg_log_sanction_bonus
AFTER INSERT OR UPDATE OR DELETE ON has_sanctionreward -- הרחבה לכל סוגי הפעולות
FOR EACH ROW EXECUTE FUNCTION log_sanction_bonus();
