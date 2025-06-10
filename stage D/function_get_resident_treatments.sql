
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
    v_treatment_cursor refcursor;
    v_log_status VARCHAR(50); -- משתנה לאחסון סטטוס הלוג
    v_log_id INT; -- לאחסון ה-ID של רשומת הלוג
BEGIN
    -- אתחול סטטוס הלוג ל'STARTED' והכנסת רשומת הלוג מיד.
    -- שמירת ה-log_id לעדכון מאוחר יותר.
    v_log_status := 'STARTED';
    INSERT INTO function_call_log (function_name, resident_id, status, call_timestamp)
    VALUES ('get_resident_treatments_refcursor', p_res_id, v_log_status, NOW())
    RETURNING log_id INTO v_log_id; -- קבלת ה-ID של רשומת הלוג החדשה

    -- בלוק לוגיקה ראשי עם טיפול בחריגות
    BEGIN
        -- פתיחת הקורסור המפורש עבור הלקוח
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

        -- עדכון סטטוס הלוג ל'SUCCESS' לפני החזרה
        v_log_status := 'SUCCESS';

    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            -- עדכון סטטוס הלוג לשגיאה
            v_log_status := 'NO_TREATMENTS_FOUND';
            RAISE EXCEPTION 'No treatments found for resident ID %.', p_res_id;

        WHEN OTHERS THEN
            -- עדכון סטטוס הלוג לשגיאה כללית
            v_log_status := 'FAILED: ' || SQLSTATE;
            RAISE EXCEPTION 'An error occurred while retrieving treatments for resident %: %', p_res_id, SQLERRM;
    END; -- סיום בלוק ה-BEGIN הפנימי

    -- עדכון רשומת הלוג עם הסטטוס הסופי (יופעל תמיד, גם אם הייתה שגיאה בבלוק הפנימי והתרחשה RAISE EXCEPTION)
    -- הבלוק הזה ירוץ *אחרי* שה-EXCEPTION נזרק, לכן יש לוודא שהלוג נשמר *בתוך* בלוק ה-EXCEPTION עצמו
    -- או להשתמש בבלוק EXCEPTION חיצוני יותר.
    -- בתיקון זה, נבצע את ה-UPDATE של הלוג בתוך בלוק ה-EXCEPTION עצמו, כיוון ש-RAISE EXCEPTION יצא מהפונקציה.
    -- אם הגענו לכאן, הפונקציה לא זרקה שגיאה ויש לנו SUCCESS.
    -- אם היתה שגיאה בבלוק הפנימי, הפונקציה היתה יוצאת עם RAISE EXCEPTION כבר שם.

    -- רק אם הפונקציה לא נזרקה עם שגיאה, נעדכן את הלוג ל'SUCCESS'.
    -- (ה-RAISE EXCEPTION בבלוק הפנימי מונע הגעה לכאן במקרה של שגיאה)
    UPDATE function_call_log
    SET status = v_log_status
    WHERE log_id = v_log_id;

    RETURN v_treatment_cursor;
END;
$$ LANGUAGE plpgsql;
-----------------------------------------------------------------------------------
DO $$
DECLARE
    -- משתנה שיכיל את ה-refcursor שחוזר מהפונקציה
    cur_result refcursor;
    -- משתנה מסוג RECORD שיכיל כל שורה שנשלפת מהקורסור
    r RECORD;
BEGIN
    -- קריאה לפונקציה שלך והקצאת ה-refcursor למשתנה cur_result
    -- החלף את '1' במזהה דייר קיים בטבלת residents שלך
    -- ו-NULL::VARCHAR אם אינך רוצה לסנן לפי סטטוס
    cur_result := get_resident_treatments_refcursor(1, NULL::VARCHAR);

    -- לולאה לשליפה והצגת הנתונים מהקורסור
    LOOP
        -- שלוף את השורה הבאה מהקורסור לתוך המשתנה r
        FETCH cur_result INTO r;

        -- צא מהלולאה אם לא נמצאו יותר שורות
        EXIT WHEN NOT FOUND;

        -- הצגת הנתונים באמצעות RAISE NOTICE
        -- הודעות אלו יופיעו בחלון ה"Messages" או בפלט הקונסולה שלך
        RAISE NOTICE 'טיפול: %, מזהה רופא: %, שם רופא: %, מטרה: %, סטטוס: %',
                     r.treatmentdate, r.doctor_id, r.doctor_name, r.purpose, r.status;
    END LOOP;

    -- סגור את הקורסור כדי לשחרר משאבים
    CLOSE cur_result;

EXCEPTION
    -- טיפול בחריגות כלליות שעלולות לקרות במהלך הרצת בלוק ה-DO
    WHEN OTHERS THEN
        RAISE NOTICE 'שגיאה בהרצת בלוק הבדיקה: %', SQLERRM;
        -- וודא שהקורסור נסגר גם במקרה של שגיאה
        IF cur_result IS NOT NULL THEN
            CLOSE cur_result;
        END IF;
END;
$$ LANGUAGE plpgsql;
