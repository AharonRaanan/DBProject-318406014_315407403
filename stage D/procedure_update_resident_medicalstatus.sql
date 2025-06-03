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
