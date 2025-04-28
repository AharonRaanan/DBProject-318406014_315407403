CREATE TABLE Doctors
(
  Doc_id INT NOT NULL,
  Doc_fName VARCHAR(20) NOT NULL,
  Doc_lName VARCHAR(20) NOT NULL,
  Specialization VARCHAR(30) NOT NULL,
  HireDate DATE NOT NULL,
  LicenseRenewalDate_ DATE NOT NULL,
  Phone VARCHAR(12) NOT NULL,
  Email VARCHAR(30) NOT NULL,
  PRIMARY KEY (Doc_id)
);

CREATE TABLE Residents
(
  ResidentID INT NOT NULL,
  R_fName VARCHAR(20) NOT NULL,
  R_lName VARCHAR(20) NOT NULL,
  Gender VARCHAR(10) NOT NULL,
  BirthDate DATE NOT NULL,
  AdmissionDate DATE NOT NULL,
  MedicalStatus VARCHAR(100) NOT NULL,
  RoomNumber INT NOT NULL,
  PRIMARY KEY (ResidentID)
);

CREATE TABLE Medications
(
  MedicationID INT NOT NULL,
  M_Name VARCHAR(30) NOT NULL,
  Dosage VARCHAR(50) NOT NULL,
  Form VARCHAR(50) NOT NULL,
  Manufacturer VARCHAR(100) NOT NULL,
  ApprovalDate DATE NOT NULL,
  ExpiryDate DATE NOT NULL,
  PRIMARY KEY (MedicationID)
);

CREATE TABLE ResidentMedications_
(
  S_date DATE NOT NULL,
  E_date DATE NOT NULL,
  Frequency VARCHAR(50) NOT NULL,
  PrescribedBy INT NOT NULL,
  ResidentMedicationID INT NOT NULL,
  ResidentID INT NOT NULL,
  MedicationID INT NOT NULL,
  PRIMARY KEY (ResidentMedicationID),
  FOREIGN KEY (ResidentID) REFERENCES Residents(ResidentID),
  FOREIGN KEY (MedicationID) REFERENCES Medications(MedicationID),
  UNIQUE (ResidentID, MedicationID)
);

CREATE TABLE MedicalTreatments
(
  TreatmentDate DATE NOT NULL,
  TreatmentType VARCHAR(100) NOT NULL,
  Notes VARCHAR(300) NOT NULL,
  TreatmentID INT NOT NULL,
  FollowUpDate_ DATE NOT NULL,
  ResidentID INT NOT NULL,
  Doc_id INT NOT NULL,
  PRIMARY KEY (TreatmentID),
  FOREIGN KEY (ResidentID) REFERENCES Residents(ResidentID),
  FOREIGN KEY (Doc_id) REFERENCES Doctors(Doc_id),
  UNIQUE (ResidentID, Doc_id)
);

CREATE TABLE Appointments
(
  AppointmentID INT NOT NULL,
  AppointmentDate DATE NOT NULL,
  Purpose VARCHAR(200) NOT NULL,
  Status VARCHAR(50) NOT NULL,
  AppointmentTime VARCHAR(20) NOT NULL,
  ResidentID INT NOT NULL,
  Doc_id INT NOT NULL,
  PRIMARY KEY (AppointmentID),
  FOREIGN KEY (ResidentID) REFERENCES Residents(ResidentID),
  FOREIGN KEY (Doc_id) REFERENCES Doctors(Doc_id),
  UNIQUE (ResidentID, Doc_id)
);
