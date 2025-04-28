1
SELECT r.resident_id, r.r_fname AS first_name, r.r_lname AS last_name, COUNT(m.equipment_id) AS total_devices
FROM residents r
JOIN medicalequipmentreceiving m ON r.resident_id = m.resident_id
GROUP BY r.resident_id, r.r_fname, r.r_lname
HAVING COUNT(m.equipment_id) > 4
ORDER BY r.resident_id;

2
SELECT 
    equipment_type, 
    COUNT(equipment_id) AS total_rentals
FROM 
    medicalequipmentreceiving
GROUP BY 
    equipment_type
HAVING 
    COUNT(equipment_id) >= ALL (
        SELECT 
            COUNT(equipment_id)
        FROM 
            medicalequipmentreceiving
        GROUP BY 
            equipment_type
    );
3
SELECT 
    COUNT(*) AS currently_rented_devices
FROM 
    medicalequipmentreceiving
WHERE 
    end_date IS NULL;

4
SELECT 
    d.doc_id, 
    d.doc_fname AS first_name, 
    d.doc_lname AS last_name,
    COUNT(mt.treatmenttime) AS total_treatments
FROM 
    doctors d
JOIN 
    medicaltreatments mt ON d.doc_id = mt.doc_id
WHERE 
    d.doc_id IN (
        SELECT 
            mt.doc_id
        FROM 
            medicaltreatments mt
        GROUP BY 
            mt.doc_id
        HAVING 
            COUNT(mt.treatmenttime) >= ALL (
                SELECT 
                    COUNT(mtt.doc_id)
                FROM 
                    medicaltreatments mtt
                GROUP BY 
                    mtt.doc_id
            )
    )
GROUP BY 
    d.doc_id, d.doc_fname, d.doc_lname
ORDER BY 
    total_treatments DESC;

5
SELECT
  COALESCE(r.year, t.year) AS year,
  COALESCE(total_devices, 0) AS total_devices,
  COALESCE(total_visits, 0) AS total_visits
FROM
  (
    SELECT EXTRACT(YEAR FROM start_date) AS year, COUNT(*) AS total_devices
    FROM medicalequipmentreceiving
    GROUP BY year
  ) AS r
FULL OUTER JOIN
  (
    SELECT EXTRACT(YEAR FROM treatmentdate) AS year, COUNT(*) AS total_visits
    FROM medicaltreatments
    GROUP BY year
  ) AS t
ON r.year = t.year
ORDER BY year;

6
SELECT resident_id, r_fname, r_lname, COUNT(medication_id) AS total_medications
FROM residentmedications
NATURAL JOIN residents
GROUP BY resident_id, r_fname, r_lname
ORDER BY total_medications DESC, resident_id;


7
SELECT 
    residents.resident_id AS resident_id,
    r_fname AS first_name,
    r_lname AS last_name,
    birthdate AS date_of_birth,
    treatmentdate AS treatment_date,
    medicaltreatments.doc_id AS doctor_id,
    doc_fname AS doctor_first_name,
    doc_lname AS doctor_last_name,
    equipment_type AS equipment_type,
    m_name AS medication_name
FROM 
    residents
LEFT JOIN medicaltreatments 
    ON residents.resident_id = medicaltreatments.resident_id
LEFT JOIN doctors 
    ON medicaltreatments.doc_id = doctors.doc_id
LEFT JOIN medicalequipmentreceiving 
    ON residents.resident_id = medicalequipmentreceiving.resident_id
LEFT JOIN residentmedications 
    ON residents.resident_id = residentmedications.resident_id
LEFT JOIN medications 
    ON residentmedications.medication_id = medications.medication_id
WHERE 
    birthdate <= ALL (
        SELECT birthdate FROM residents
    )
GROUP BY 
    residents.resident_id,
    r_fname,
    r_lname,
    birthdate,
    treatmentdate,
    medicaltreatments.doc_id,
    doc_fname,
    doc_lname,
    equipment_type,
    m_name;

8
SELECT 
    residents.resident_id AS resident_id,
    r_fname AS first_name,
    r_lname AS last_name,
    birthdate AS date_of_birth,
    treatmentdate AS treatment_date,
    purpose AS treatment_purpose,
    doc_fname AS doctor_first_name,
    doc_lname AS doctor_last_name
FROM 
    residents
LEFT JOIN medicaltreatments 
    ON residents.resident_id = medicaltreatments.resident_id
LEFT JOIN doctors 
    ON medicaltreatments.doc_id = doctors.doc_id
GROUP BY 
    residents.resident_id,
    r_fname,
    r_lname,
    birthdate,
    treatmentdate,
    doc_fname,
    doc_lname,
    purpose
ORDER BY 
    residents.resident_id,
    treatmentdate;
