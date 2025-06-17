-- פרוצדורה לעדכון סטטוס תרופות של דיירים לפי תאריך חתך נתון


CREATE OR REPLACE PROCEDURE update_resident_medication_status(cutoff_date DATE)
LANGUAGE plpgsql
AS $$
DECLARE
    rec RECORD;
    updated_count INT := 0;
BEGIN
    RAISE NOTICE 'מעדכן סטטוס תרופות עד תאריך %', cutoff_date;

    -- סריקה של תרופות שהסטטוס שלהן פעיל
    FOR rec IN 
        SELECT residentmedication_id, resident_id, medication_id, s_date, e_date, status
        FROM residentmedications
        WHERE status = 'active'
    LOOP
        BEGIN
            -- אם תאריך סיום קטן מה cutoff, מעדכנים ל-inactive
            IF rec.e_date IS NOT NULL AND rec.e_date < cutoff_date THEN
                UPDATE residentmedications
                SET status = 'inactive'
                WHERE residentmedication_id = rec.residentmedication_id;

                INSERT INTO resident_medication_log(resident_id, medication_id, action)
                VALUES (rec.resident_id, rec.medication_id, 'Set medication inactive due to end date');

                updated_count := updated_count + 1;

                RAISE NOTICE 'עדכון תרופה % לדייר % כלא פעילה', rec.medication_id, rec.resident_id;
            END IF;

        EXCEPTION WHEN OTHERS THEN
            RAISE WARNING 'שגיאה בעדכון תרופה % לדייר %: %', rec.medication_id, rec.resident_id, SQLERRM;
        END;
    END LOOP;

    RAISE NOTICE 'סה"כ תרופות עודכנו: %', updated_count;
END;
$$;

--------------------------------------------------------------------
CALL update_resident_medication_status('2024-06-02');
