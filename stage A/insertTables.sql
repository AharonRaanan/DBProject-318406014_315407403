INSERT INTO Doctors (Doc_id, Doc_fName, Doc_lName, Specialization, HireDate, LicenseRenewalDate_, Phone, Email)
VALUES
(1, 'John', 'Doe', 'Cardiology', '2010-05-01', '2025-05-01', '555-1234', 'john.doe@example.com'),
(2, 'Jane', 'Smith', 'Neurology', '2015-08-12', '2025-08-12', '555-5678', 'jane.smith@example.com'),
(3, 'Emily', 'Johnson', 'Pediatrics', '2018-11-25', '2025-11-25', '555-8765', 'emily.johnson@example.com');

INSERT INTO Residents (ResidentID, R_fName, R_lName, Gender, BirthDate, AdmissionDate, MedicalStatus, RoomNumber)
VALUES
(1, 'Alice', 'Brown', 'Female', '1945-06-30', '2025-01-15', 'Healthy', 101),
(2, 'Bob', 'Green', 'Male', '1955-07-22', '2025-02-01', 'Chronic illness', 102),
(3, 'Charlie', 'Davis', 'Male', '1965-08-05', '2025-03-10', 'Recovering from surgery', 103);

INSERT INTO Medications (MedicationID, M_Name, Dosage, Form, Manufacturer, ApprovalDate, ExpiryDate)
VALUES
(1, 'Aspirin', '50mg', 'Tablet', 'PharmaCo', '2022-01-01', '2025-01-01'),
(2, 'Ibuprofen', '200mg', 'Tablet', 'HealthInc', '2023-05-01', '2026-05-01'),
(3, 'Paracetamol', '500mg', 'Capsule', 'MedGlobal', '2021-09-15', '2024-09-15');

INSERT INTO ResidentMedications_ (S_date, E_date, Frequency, PrescribedBy, ResidentMedicationID, ResidentID, MedicationID)
VALUES
('2025-01-15', '2025-02-15', 'Daily', 1, 1, 1, 1),
('2025-02-01', '2025-03-01', 'Every other day', 2, 2, 2, 2),
('2025-03-10', '2025-04-10', 'Twice a day', 3, 3, 3, 3);

INSERT INTO MedicalTreatments (TreatmentDate, TreatmentType, Notes, TreatmentID, FollowUpDate_, ResidentID, Doc_id)
VALUES
('2025-01-20', 'Physiotherapy', 'Post-surgery recovery', 1, '2025-02-20', 1, 1),
('2025-02-10', 'Surgery', 'Knee replacement', 2, '2025-03-10', 2, 2),
('2025-03-15', 'Consultation', 'Routine checkup', 3, '2025-04-15', 3, 3);

INSERT INTO Appointments (AppointmentID, AppointmentDate, Purpose, Status, AppointmentTime, ResidentID, Doc_id)
VALUES
(1, '2025-01-20', 'Routine Checkup', 'Completed', '09:00', 1, 1),
(2, '2025-02-10', 'Surgery Consultation', 'Scheduled', '11:00', 2, 2),
(3, '2025-03-15', 'Follow-up Consultation', 'Completed', '14:00', 3, 3);
