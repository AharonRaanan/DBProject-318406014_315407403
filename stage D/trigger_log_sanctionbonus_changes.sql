-- טריגר המתעדכן בעת הוספה או שינוי של נתוני מענקים או סנקציות, לרישום היסטוריית שינויים בטבלת הלוג


CREATE TABLE IF NOT EXISTS sanctionbonus_log (
    log_id SERIAL PRIMARY KEY,
    recordid_ integer NOT NULL,
    amount_ double precision NOT NULL,
    reason character varying(150) NOT NULL,
    sanction_or_bonus_ character(1) NOT NULL,
    dategiven date NOT NULL,
    action_type VARCHAR(10) NOT NULL,  -- 'INSERT', 'UPDATE', 'DELETE'
    action_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
---------------------------------
CREATE OR REPLACE FUNCTION log_sanctionbonus_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF (TG_OP = 'INSERT') THEN
        INSERT INTO sanctionbonus_log(recordid_, amount_, reason, sanction_or_bonus_, dategiven, action_type)
        VALUES (NEW.recordid_, NEW.amount_, NEW.reason, NEW.sanction_or_bonus_, NEW.dategiven, 'INSERT');
        RETURN NEW;
    ELSIF (TG_OP = 'UPDATE') THEN
        INSERT INTO sanctionbonus_log(recordid_, amount_, reason, sanction_or_bonus_, dategiven, action_type)
        VALUES (NEW.recordid_, NEW.amount_, NEW.reason, NEW.sanction_or_bonus_, NEW.dategiven, 'UPDATE');
        RETURN NEW;
    ELSIF (TG_OP = 'DELETE') THEN
        INSERT INTO sanctionbonus_log(recordid_, amount_, reason, sanction_or_bonus_, dategiven, action_type)
        VALUES (OLD.recordid_, OLD.amount_, OLD.reason, OLD.sanction_or_bonus_, OLD.dategiven, 'DELETE');
        RETURN OLD;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;
------------------------------------
CREATE TRIGGER trg_sanctionbonus_log
AFTER INSERT OR UPDATE OR DELETE ON sanctionbonus
FOR EACH ROW
EXECUTE FUNCTION log_sanctionbonus_changes();
