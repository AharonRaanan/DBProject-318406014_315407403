CREATE OR REPLACE PROCEDURE add_sanction_bonus(emp_id INT, is_bonus BOOLEAN, reason TEXT, amount DOUBLE PRECISION)
LANGUAGE plpgsql
AS $$
DECLARE
    new_recordid INT;
BEGIN
    new_recordid := (SELECT COALESCE(MAX(recordid_), 0) + 1 FROM sanctionbonus);

    INSERT INTO sanctionbonus(recordid_, amount_, reason, sanction_or_bonus_, dategiven)
    VALUES (new_recordid, amount, reason, CASE WHEN is_bonus THEN 'B' ELSE 'S' END, CURRENT_DATE);

    INSERT INTO has_sanctionreward(recordid_, employeeid_, date_)
    VALUES (new_recordid, emp_id, CURRENT_DATE);
END;
$$;
