CREATE OR REPLACE PROCEDURE update_resident_medicalstatus()
LANGUAGE plpgsql
AS $$
DECLARE
    rec RECORD;
    age INT;
BEGIN
    FOR rec IN SELECT resident_id, birthdate FROM residents
    LOOP
        age := DATE_PART('year', CURRENT_DATE) - DATE_PART('year', rec.birthdate);
        
        IF age >= 85 THEN
            UPDATE residents SET medicalstatus = 'High-Risk Elderly' WHERE resident_id = rec.resident_id;
        ELSIF age >= 65 THEN
            UPDATE residents SET medicalstatus = 'Senior' WHERE resident_id = rec.resident_id;
        ELSE
            UPDATE residents SET medicalstatus = 'Adult' WHERE resident_id = rec.resident_id;
        END IF;
    END LOOP;
END;
$$;
-------------------------------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE update_resident_medicalstatus()
LANGUAGE plpgsql
AS $$
DECLARE
    -- הגדרת קורסור מפורש
    -- FOR UPDATE מבטיח שהשורות שיישלפו יהיו נעולות לעדכון בלעדי שלנו
    cur_residents CURSOR FOR
        SELECT resident_id, birthdate, medicalstatus
        FROM residents
        ORDER BY resident_id
        FOR UPDATE; -- חשוב: locks rows for update

    -- משתנה מסוג RECORD ללכידת שורות הקורסור
    v_resident_record RECORD;
    v_age INT;
    v_updated_status TEXT;
    v_updated_count INT := 0; -- מונה לעדכונים מוצלחים
    v_original_status TEXT; -- לשימור הסטטוס המקורי לבדיקה
BEGIN
    -- בלוק לטיפול כללי בחריגות
    BEGIN
        -- פתיחת הקורסור
        OPEN cur_residents;

        LOOP
            -- שליפת שורה מהקורסור לתוך המשתנה RECORD
            FETCH cur_residents INTO v_resident_record;

            -- יציאה מהלולאה אם לא נמצאו יותר שורות
            EXIT WHEN NOT FOUND;

            -- טיפול אפשרי בחריגות ספציפיות בתוך הלולאה (לדוגמה, אם תאריך הלידה NULL)
            BEGIN
                -- בדיקה אם תאריך הלידה קיים
                IF v_resident_record.birthdate IS NULL THEN
                    RAISE WARNING 'Skipping resident ID %: Birthdate is missing.', v_resident_record.resident_id;
                    CONTINUE; -- דילוג על שורה זו והמשך לשורה הבאה
                END IF;

                -- חישוב הגיל
                v_age := DATE_PART('year', CURRENT_DATE) - DATE_PART('year', v_resident_record.birthdate);

                -- שמירת הסטטוס המקורי לפני העדכון (אם נרצה להשוות)
                v_original_status := v_resident_record.medicalstatus;

                -- לוגיקה של הסתעפויות לעדכון הסטטוס הרפואי
                IF v_age >= 85 THEN
                    v_updated_status := 'High-Risk Elderly';
                ELSIF v_age >= 65 THEN
                    v_updated_status := 'Senior';
                ELSE
                    v_updated_status := 'Adult';
                END IF;

                -- בדיקה האם הסטטוס אכן השתנה לפני ביצוע UPDATE מיותר (אופטימיזציה)
                IF v_original_status IS DISTINCT FROM v_updated_status THEN
                    -- ביצוע עדכון על השורה הנוכחית באמצעות WHERE CURRENT OF
                    -- WHERE CURRENT OF CURSOR_NAME מאפשר לעדכן את השורה שנשלפה כרגע בקורסור
                    UPDATE residents
                    SET medicalstatus = v_updated_status
                    WHERE CURRENT OF cur_residents; -- שימוש ב-CURRENT OF

                    v_updated_count := v_updated_count + 1;
                    -- RAISE NOTICE 'Updated resident % from % to %', v_resident_record.resident_id, v_original_status, v_updated_status;
                END IF;

            EXCEPTION
                WHEN OTHERS THEN
                    -- טיפול בשגיאות שעלולות לקרות עבור דייר ספציפי בתוך הלולאה
                    RAISE WARNING 'Error processing resident ID %: %', v_resident_record.resident_id, SQLERRM;
                    -- נמשיך לדייר הבא במקום לעצור את כל הפרוצדורה
            END; -- סיום בלוק ה-EXCEPTION הפנימי
        END LOOP;

        -- סגירת הקורסור לאחר סיום הלולאה
        CLOSE cur_residents;

        -- הודעת סיכום על כמות העדכונים
        RAISE NOTICE 'Medical status update complete. % residents updated.', v_updated_count;

    EXCEPTION
        WHEN OTHERS THEN
            -- טיפול בחריגות כלליות שיכולות לקרות מחוץ ללולאה (לדוגמה, בעיות גישה לטבלה)
            IF CURSOR_IS_OPEN('cur_residents') THEN
                CLOSE cur_residents; -- וודא שהקורסור נסגר במקרה של שגיאה
            END IF;
            RAISE EXCEPTION 'An unexpected error occurred during medical status update: %', SQLERRM;
    END;
END;
$$;
