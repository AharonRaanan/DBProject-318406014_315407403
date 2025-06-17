-- טריגר המתעדכן בעת שינוי כתובת מייל או טלפון של רופא, ושומר היסטוריית שינויים בטבלת הלוג


-- יצירת טבלת הלוג עם שמות פרטי ומשפחה
CREATE TABLE IF NOT EXISTS doctors_email_log (
    log_id SERIAL PRIMARY KEY,
    doctor_id INT NOT NULL,
    doctor_first_name VARCHAR,
    doctor_last_name VARCHAR,
    old_email VARCHAR,
    new_email VARCHAR,
    old_phone VARCHAR,
    new_phone VARCHAR,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- יצירת פונקציית הטריגר שמתעדכנת בשינוי מייל או טלפון
CREATE OR REPLACE FUNCTION log_doctors_contact_changes()
RETURNS TRIGGER AS $$
DECLARE
    first_name VARCHAR;
    last_name VARCHAR;
BEGIN
    -- משיכת שם פרטי ושם משפחה מטבלת העובדים
    SELECT firstname_, lastname_ INTO first_name, last_name
    FROM employee
    WHERE employeeid_ = NEW.employeeid_;

    -- הוספת רשומה ללוג עם כל הפרטים לפני ואחרי השינוי
    INSERT INTO doctors_email_log(
        doctor_id,
        doctor_first_name,
        doctor_last_name,
        old_email,
        new_email,
        old_phone,
        new_phone,
        changed_at
    )
    VALUES (
        NEW.employeeid_,
        first_name,
        last_name,
        OLD.email,
        NEW.email,
        OLD.phone,
        NEW.phone,
        CURRENT_TIMESTAMP
    );

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- יצירת הטריגר על טבלת doctors שמאזין לעדכונים בעמודות email או phone
CREATE TRIGGER doctors_contact_update_trigger
AFTER UPDATE OF email, phone ON doctors
FOR EACH ROW
WHEN (OLD.email IS DISTINCT FROM NEW.email OR OLD.phone IS DISTINCT FROM NEW.phone)
EXECUTE FUNCTION log_doctors_contact_changes();
