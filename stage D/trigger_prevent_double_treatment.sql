CREATE OR REPLACE FUNCTION prevent_double_treatment()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM medicaltreatments
        WHERE resident_id = NEW.resident_id
        AND treatmentdate = NEW.treatmentdate
        AND treatmenttime = NEW.treatmenttime
    ) THEN
        RAISE EXCEPTION 'Resident % already has a treatment scheduled on % at %',
            NEW.resident_id, NEW.treatmentdate, NEW.treatmenttime;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_prevent_double_treatment
BEFORE INSERT ON medicaltreatments
FOR EACH ROW EXECUTE FUNCTION prevent_double_treatment();
