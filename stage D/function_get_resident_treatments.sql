
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
