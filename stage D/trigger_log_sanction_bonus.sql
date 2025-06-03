CREATE TABLE IF NOT EXISTS sanction_log (
    log_id SERIAL PRIMARY KEY,
    employeeid_ INT,
    recordid_ INT,
    log_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    action_type TEXT
);
--------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION log_sanction_bonus()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO sanction_log(employeeid_, recordid_, action_type)
    VALUES (NEW.employeeid_, NEW.recordid_, 'INSERT');

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_log_sanction_bonus
AFTER INSERT ON has_sanctionreward
FOR EACH ROW EXECUTE FUNCTION log_sanction_bonus();
