-- פונקציה לסיכום דיירים לפי ציוד 

CREATE OR REPLACE FUNCTION get_equipment_residents_summary(
    min_devices INT,
    min_rentals INT,
    min_current_rentals INT
)
RETURNS TABLE (
    category TEXT,
    resident_id INT,
    resident_first_name VARCHAR,
    resident_last_name VARCHAR,
    total_devices BIGINT,
    most_rented_type VARCHAR,
    total_rentals BIGINT,
    current_rented_type VARCHAR,
    current_rental_count BIGINT
) AS $$
DECLARE
    rec RECORD;
    count_devices INT := 0;
    count_rentals INT := 0;
    count_current INT := 0;
BEGIN
    -- כותרת חלק 1
    RAISE NOTICE E'\n=== חלק 1: דיירים עם יותר מ־% מכשירים מושאלים ===', min_devices;

    FOR rec IN
        SELECT r.resident_id, r.r_fname, r.r_lname, COUNT(m.equipment_id) AS total_devices
        FROM residents r
        JOIN medicalequipmentreceiving m ON r.resident_id = m.resident_id
        GROUP BY r.resident_id, r.r_fname, r.r_lname
        HAVING COUNT(m.equipment_id) > min_devices
    LOOP
        count_devices := count_devices + 1;

        category := 'ResidentsWithDevices';
        resident_id := rec.resident_id;
        resident_first_name := rec.r_fname;
        resident_last_name := rec.r_lname;
        total_devices := rec.total_devices;
        most_rented_type := NULL;
        total_rentals := NULL;
        current_rented_type := NULL;
        current_rental_count := NULL;

        RAISE NOTICE 'דייר: % % (ID: %) - כמות מכשירים: %',
            rec.r_fname, rec.r_lname, rec.resident_id, rec.total_devices;

        RETURN NEXT;
    END LOOP;

    IF count_devices = 0 THEN
        RAISE NOTICE 'לא נמצאו דיירים עם יותר מ־% מכשירים.', min_devices;
    END IF;

    -- כותרת חלק 2
    RAISE NOTICE E'\n=== חלק 2: סוגי מכשירים שמושאלים לפחות % פעמים ===', min_rentals;

    FOR rec IN
        SELECT equipment_type, COUNT(equipment_id) AS total_rentals
        FROM medicalequipmentreceiving
        GROUP BY equipment_type
        HAVING COUNT(equipment_id) >= min_rentals
    LOOP
        count_rentals := count_rentals + 1;

        category := 'MostRentedDevices';
        resident_id := NULL;
        resident_first_name := NULL;
        resident_last_name := NULL;
        total_devices := NULL;
        most_rented_type := rec.equipment_type;
        total_rentals := rec.total_rentals;
        current_rented_type := NULL;
        current_rental_count := NULL;

        RAISE NOTICE 'סוג מכשיר: % - סה"כ השאלות: %',
            rec.equipment_type, rec.total_rentals;

        RETURN NEXT;
    END LOOP;

    IF count_rentals = 0 THEN
        RAISE NOTICE 'לא נמצאו מכשירים עם יותר מ־% השאלות.', min_rentals;
    END IF;

    -- כותרת חלק 3
    RAISE NOTICE E'\n=== חלק 3: מכשירים בהשאלה פעילה לפי סוג (לפחות % השאלות פעילות) ===', min_current_rentals;

    FOR rec IN
        SELECT equipment_type, COUNT(*) AS current_rental_count
        FROM medicalequipmentreceiving
        WHERE end_date IS NULL
        GROUP BY equipment_type
        HAVING COUNT(*) >= min_current_rentals
    LOOP
        count_current := count_current + 1;

        category := 'CurrentRentalsByType';
        resident_id := NULL;
        resident_first_name := NULL;
        resident_last_name := NULL;
        total_devices := NULL;
        most_rented_type := NULL;
        total_rentals := NULL;
        current_rented_type := rec.equipment_type;
        current_rental_count := rec.current_rental_count;

        RAISE NOTICE 'השאלות פעילות - סוג: % - כמות: %',
            rec.equipment_type, rec.current_rental_count;

        RETURN NEXT;
    END LOOP;

    IF count_current = 0 THEN
        RAISE NOTICE 'לא נמצאו מכשירים מושאלים כרגע עם יותר מ־% השאלות פעילות.', min_current_rentals;
    END IF;
END;
$$ LANGUAGE plpgsql;
---------------------------------------------------------------------
SELECT * FROM get_equipment_residents_summary(3, 5, 2);
