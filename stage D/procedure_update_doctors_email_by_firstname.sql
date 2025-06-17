CREATE OR REPLACE PROCEDURE update_doctors_email_by_firstname()
LANGUAGE plpgsql
AS $$
DECLARE
    rec RECORD;
    new_email TEXT;
BEGIN
    FOR rec IN
        SELECT d.employeeid_, d.email, e.firstname_
        FROM doctors d
        JOIN employee e ON d.employeeid_ = e.employeeid_
    LOOP
        BEGIN
            new_email := rec.firstname_ || '@hospital.org';

            -- בדיקה אם האימייל שונה מהנדרש
            IF rec.email IS DISTINCT FROM new_email THEN
                UPDATE doctors
                SET email = new_email
                WHERE employeeid_ = rec.employeeid_;

                RAISE NOTICE 'עודכן אימייל לרופא % ל- %', rec.employeeid_, new_email;
            ELSE
                RAISE NOTICE 'האימייל של רופא % כבר מעודכן', rec.employeeid_;
            END IF;

        EXCEPTION WHEN OTHERS THEN
            RAISE WARNING 'שגיאה בעדכון אימייל לרופא %: %', rec.employeeid_, SQLERRM;
        END;
    END LOOP;
END;
$$;
-------------------------------------------------------------------
CALL update_doctors_email_by_firstname();
