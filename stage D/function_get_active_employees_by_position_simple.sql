DROP FUNCTION IF EXISTS get_active_employees_by_position_simple(integer);

CREATE OR REPLACE FUNCTION get_active_employees_by_position_simple(p_positionid INT)
RETURNS SETOF employee
AS $$
DECLARE
    emp_rec employee%ROWTYPE;
BEGIN
    FOR emp_rec IN
        SELECT *
        FROM employee
        WHERE active = true AND positionid_ = p_positionid
    LOOP
        RAISE NOTICE 'Found employee: % % (ID: %)', emp_rec.firstname_, emp_rec.lastname_, emp_rec.employeeid_;
        RETURN NEXT emp_rec;
    END LOOP;
END;
$$ LANGUAGE plpgsql;
-----------------------------------------------
SELECT * FROM get_active_employees_by_position_simple(Choose a number);
