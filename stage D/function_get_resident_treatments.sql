
CREATE OR REPLACE FUNCTION get_resident_treatments(res_id INT)
RETURNS TABLE (
    treatmentdate DATE,
    doctor_id INT,
    doctor_name VARCHAR,
    purpose VARCHAR,
    status VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        mt.treatmentdate,
        mt.employeeid_ AS doctor_id,
        (e.firstname_ || ' ' || e.lastname_)::VARCHAR AS doctor_name,
        mt.purpose,
        mt.status
    FROM medicaltreatments mt
    JOIN doctors d ON mt.employeeid_ = d.employeeid_
    JOIN employee e ON d.employeeid_ = e.employeeid_
    WHERE mt.resident_id = res_id
    ORDER BY mt.treatmentdate DESC;
END;
$$ LANGUAGE plpgsql;
---------------------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION get_resident_treatments_refcursor(
    p_res_id INT,
    p_status_filter VARCHAR DEFAULT NULL
)
RETURNS refcursor AS $$
DECLARE
    -- הגדרת REF CURSOR שיחזור מחוץ לפונקציה
    v_treatment_cursor refcursor;

    -- משתנים ללוגיקה פנימית (דוגמה לשימוש ברשומה ובלולאה)
    v_treatment_record RECORD; -- משתנה כללי לשימוש בלולאת הקורסור
    v_treatment_count INT := 0; -- ספירת טיפולים שנמצאו
    v_log_status VARCHAR(50);
BEGIN
    -- טיפול בחריגות לכלל הפונקציה
    BEGIN
        -- רישום קריאה לפונקציה (דוגמה ל-DML בתוך פונקציה)
        INSERT INTO function_call_log (function_name, resident_id, status)
        VALUES ('get_resident_treatments_refcursor', p_res_id, 'STARTED');

        -- הגדרת קורסור מפורש
        -- שימו לב: הקורסור מוגדר עבור שאילתה מסוימת
        -- הוא לא נפתח כאן, אלא יוחזר כרפרנס
        OPEN v_treatment_cursor FOR
            SELECT
                mt.treatmentdate,
                mt.employeeid_ AS doctor_id,
                (e.firstname_ || ' ' || e.lastname_)::VARCHAR AS doctor_name,
                mt.purpose,
                mt.status
            FROM medicaltreatments mt
            JOIN doctors d ON mt.employeeid_ = d.employeeid_
            JOIN employee e ON d.employeeid_ = e.employeeid_
            WHERE mt.resident_id = p_res_id
            -- הסתעפות: אם יש פילטר סטטוס, נוסיף אותו לשאילתה
            AND (p_status_filter IS NULL OR mt.status = p_status_filter)
            ORDER BY mt.treatmentdate DESC;

        -- דוגמה לשימוש בקורסור *בתוך* הפונקציה (לא חובה, אבל מדגים explicit cursor ולולאה)
        -- אם נרצה לעבד את הנתונים לפני החזרת הקורסור
        -- (הערה: לשם הדגמה בלבד, בדרך כלל לא תעשה זאת עם REF CURSOR שמיועד להחזרה ללקוח)
        LOOP
            FETCH v_treatment_cursor INTO v_treatment_record;
            EXIT WHEN NOT FOUND; -- יציאה מהלולאה אם אין יותר שורות

            v_treatment_count := v_treatment_count + 1;

            -- הסתעפות נוספת: בדיקת סטטוס טיפול
            IF v_treatment_record.status = 'Completed' THEN
                -- RAISE NOTICE 'Found a completed treatment for resident % on %.', p_res_id, v_treatment_record.treatmentdate;
                -- (אפשר לעשות פה משהו אחר, לדוגמה, עדכון טבלה אחרת)
                CONTINUE; -- המשך לטיפול הבא
            END IF;
        END LOOP;

        -- לאחר ספירת הטיפולים, סגור את הקורסור הנוכחי
        -- ואז פתח אותו מחדש כדי להחזיר אותו ללקוח במצב "נקי" (כי עברנו עליו כבר בלולאה)
        CLOSE v_treatment_cursor;

        -- פתח מחדש את הקורסור כדי להחזיר אותו כ-REF CURSOR ללקוח
        OPEN v_treatment_cursor FOR
            SELECT
                mt.treatmentdate,
                mt.employeeid_ AS doctor_id,
                (e.firstname_ || ' ' || e.lastname_)::VARCHAR AS doctor_name,
                mt.purpose,
                mt.status
            FROM medicaltreatments mt
            JOIN doctors d ON mt.employeeid_ = d.employeeid_
            JOIN employee e ON d.employeeid_ = e.employeeid_
            WHERE mt.resident_id = p_res_id
            AND (p_status_filter IS NULL OR mt.status = p_status_filter)
            ORDER BY mt.treatmentdate DESC;

        -- רישום סיום מוצלח
        v_log_status := 'SUCCESS';
        RETURN v_treatment_cursor;

    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            -- אם לא נמצאו טיפולים כלל עבור הדייר (ה-SELECT הראשון יחזיר כלום)
            v_log_status := 'NO_TREATMENTS_FOUND';
            RAISE EXCEPTION 'No treatments found for resident ID %.', p_res_id;
        WHEN OTHERS THEN
            -- טיפול כללי בכל שגיאה אחרת
            v_log_status := 'FAILED: ' || SQLSTATE; -- SQLSTATE הוא קוד שגיאה
            RAISE EXCEPTION 'An error occurred while retrieving treatments for resident %: %', p_res_id, SQLERRM;
    FINALLY
        -- ה-FINALLY בלוק ירוץ תמיד, בין אם הייתה שגיאה ובין אם לא
        -- זה מקום טוב לעדכן את הלוג הסופי
        UPDATE function_call_log
        SET status = v_log_status
        WHERE resident_id = p_res_id AND function_name = 'get_resident_treatments_refcursor'
        ORDER BY call_timestamp DESC
        LIMIT 1;
    END;
END;
$$ LANGUAGE plpgsql;
