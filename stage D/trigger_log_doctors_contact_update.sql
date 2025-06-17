-- יצירת פונקציית הטריגר
CREATE OR REPLACE FUNCTION log_doctors_contact_update()
RETURNS TRIGGER AS $$
BEGIN
    IF (NEW.email IS DISTINCT FROM OLD.email) OR (NEW.phone IS DISTINCT FROM OLD.phone) THEN
        INSERT INTO doctors_email_log(doctor_id, old_email, new_email, old_phone, new_phone, changed_at)
        VALUES (
            OLD.employeeid_,
            OLD.email,
            NEW.email,
            OLD.phone,
            NEW.phone,
            CURRENT_TIMESTAMP
        );
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- מחיקת טריגר קיים אם יש
DROP TRIGGER IF EXISTS trg_doctors_contact_update ON doctors;

-- יצירת טריגר חדש שיפעיל את הפונקציה אחרי עדכון בטבלת doctors
CREATE TRIGGER trg_doctors_contact_update
AFTER UPDATE ON doctors
FOR EACH ROW
EXECUTE FUNCTION log_doctors_contact_update();
