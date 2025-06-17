CREATE OR REPLACE FUNCTION main_function_one()
RETURNS VOID
LANGUAGE plpgsql
AS $$
DECLARE
    pos_id INT := 1;
    active_count INT;
BEGIN
    active_count := count_active_employees_by_position(pos_id);
    RAISE NOTICE 'Active employees in position %: %', pos_id, active_count;

    CALL update_doctors_email_by_firstname();

    RAISE NOTICE 'main_function_one executed successfully';
END;
$$;
-----------------------------------
SELECT main_function_one();
