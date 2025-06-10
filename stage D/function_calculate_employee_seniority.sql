CREATE OR REPLACE FUNCTION count_treatments_for_resident(res_id INT)
RETURNS TABLE(total_treatments INT, approved_treatments INT) AS
$$
BEGIN
    SELECT COUNT(*), COUNT(*) FILTER (WHERE status = 'Approved')
    INTO total_treatments, approved_treatments
    FROM medicaltreatments
    WHERE resident_id = res_id;

    RETURN NEXT;
END;
$$ LANGUAGE plpgsql;
