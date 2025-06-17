DROP FUNCTION IF EXISTS count_active_employees_by_position(INT);

CREATE OR REPLACE FUNCTION count_active_employees_by_position(min_employees INT)
RETURNS TABLE(pos_id INT, active_count BIGINT)
AS $$
DECLARE
    rec RECORD;
    found_result BOOLEAN := false;
BEGIN
    RAISE NOTICE '⏳ מתחיל לספור תפקידים עם יותר מ־% עובדים פעילים...', min_employees;

    FOR rec IN
        SELECT positionid_, COUNT(*) AS active_count
        FROM employee
        WHERE active = true
        GROUP BY positionid_
        ORDER BY positionid_
    LOOP
        IF rec.active_count > min_employees THEN
            RAISE NOTICE '✅ תפקיד % עם % עובדים פעילים – נכלל.', rec.positionid_, rec.active_count;
            pos_id := rec.positionid_;
            active_count := rec.active_count;
            found_result := true;
            RETURN NEXT;
        END IF;
    END LOOP;

    IF NOT found_result THEN
        RAISE EXCEPTION '⚠️ לא נמצא אף תפקיד עם יותר מ־% עובדים פעילים.', min_employees;
    END IF;

    RAISE NOTICE '✅ סיום.';
END;
$$ LANGUAGE plpgsql;

---------------------------------------------------------------------------------

SELECT * FROM count_active_employees_by_position(Choose a number);

