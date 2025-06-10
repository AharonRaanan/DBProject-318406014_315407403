CREATE OR REPLACE FUNCTION prevent_double_treatment()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM medicaltreatments
        WHERE resident_id = NEW.resident_id
        AND treatmentdate = NEW.treatmentdate
        AND treatmenttime = NEW.treatmenttime
    ) THEN
        RAISE EXCEPTION 'Resident % already has a treatment scheduled on % at %',
            NEW.resident_id, NEW.treatmentdate, NEW.treatmenttime;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_prevent_double_treatment
BEFORE INSERT ON medicaltreatments
FOR EACH ROW EXECUTE FUNCTION prevent_double_treatment();
----------------------------------------------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION prevent_double_treatment()
RETURNS TRIGGER AS $$
BEGIN
    -- בלוק לטיפול בחריגות
    BEGIN
        -- בדיקת כפילות (תאריך ושעה זהים)
        -- שימו לב: אם הוספתם treatmentend, תוכלו להשתמש בלוגיקה של חפיפה בזמנים (ראה הערה למטה)
        IF EXISTS (
            SELECT 1
            FROM medicaltreatments
            WHERE resident_id = NEW.resident_id
            AND treatmentdate = NEW.treatmentdate
            AND treatmenttime = NEW.treatmenttime
        ) THEN
            RAISE EXCEPTION 'Resident % already has a treatment scheduled on % at %',
                            NEW.resident_id, NEW.treatmentdate, NEW.treatmenttime;
        END IF;

        -- אופציונלי: בדיקת חפיפה בזמנים (במקום שוויון מוחלט)
        -- דורש עמודת treatmentend בטבלה
        --[[
        IF EXISTS (
            SELECT 1
            FROM medicaltreatments
            WHERE resident_id = NEW.resident_id
            AND treatmentdate = NEW.treatmentdate
            -- בדיקת חפיפה: הטיפול החדש מתחיל לפני שהקיים מסתיים, והטיפול החדש מסתיים אחרי שהקיים מתחיל
            AND NEW.treatmenttime < treatmentend
            AND NEW.treatmentend > treatmenttime
        ) THEN
            RAISE EXCEPTION 'Resident % already has a treatment scheduled that overlaps with the proposed time.',
                            NEW.resident_id;
        END IF;
        --]]

    EXCEPTION
        WHEN OTHERS THEN
            -- טיפול בשגיאות בלתי צפויות (אם כי פחות סביר כאן)
            RAISE EXCEPTION 'An unexpected error occurred while checking for double treatment: %', SQLERRM;
    END;

    -- RETURN NEW חובה לטריגר BEFORE ROW
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- הגדרת הטריגר
CREATE TRIGGER trg_prevent_double_treatment
BEFORE INSERT -- אפשר להוסיף OR UPDATE אם רוצים למנוע כפילויות גם בעדכון
ON medicaltreatments
FOR EACH ROW EXECUTE FUNCTION prevent_double_treatment();
