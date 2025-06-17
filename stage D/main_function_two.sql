CREATE OR REPLACE FUNCTION main_function_two()
RETURNS VOID
LANGUAGE plpgsql
AS $$
DECLARE
    pos_id INT := 1;
    param1 INT := 1;
    param2 INT := 2;
    param3 INT := 3;
    cutoff DATE := '2024-06-01';
BEGIN
    PERFORM get_active_employees_by_position_simple(pos_id);
    RAISE NOTICE 'Called get_active_employees_by_position_simple with position %', pos_id;

    PERFORM get_equipment_residents_summary(param1, param2, param3);
    RAISE NOTICE 'Called get_equipment_residents_summary with params %, %, %', param1, param2, param3;

    CALL update_resident_medication_status(cutoff);
    RAISE NOTICE 'Called update_resident_medication_status with cutoff date %', cutoff;

    RAISE NOTICE 'main_function_two executed successfully';
END;
$$;
-------------------------------------------------
SELECT main_function_two();
