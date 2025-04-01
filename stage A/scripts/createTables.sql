CREATE TABLE doctors
(
  doc_id INT NOT NULL,
  doc_fname VARCHAR(50) NOT NULL,
  doc_lname VARCHAR(50) NOT NULL,
  specialization VARCHAR(100) NOT NULL,
  hiredate DATE NOT NULL,
  licenserenewaldate_ DATE NOT NULL,
  phone VARCHAR(100) NOT NULL,
  email VARCHAR(100) NOT NULL,
  doc_gender VARCHAR(20) NOT NULL,
  PRIMARY KEY (Doc_id)
);

CREATE TABLE residents
(
  resident_id INT NOT NULL,
  r_fname VARCHAR(50) NOT NULL,
  r_lname VARCHAR(50) NOT NULL,
  r_gender VARCHAR(20) NOT NULL,
  birthdate DATE NOT NULL,
  admissiondate DATE NOT NULL,
  medicalstatus VARCHAR(100) NOT NULL,
  roomnumber INT NOT NULL,
  PRIMARY KEY (resident_id)
);

CREATE TABLE medications
(
  medication_id INT NOT NULL,
  m_name VARCHAR(100) NOT NULL,
  dosage VARCHAR(50) NOT NULL,
  form VARCHAR(50) NOT NULL,
  manufacturer VARCHAR(100) NOT NULL,
  approvalDate DATE NOT NULL,
  expirydate DATE NOT NULL,
  PRIMARY KEY (medication_id)
);

CREATE TABLE medicaltreatments
(
  treatmentdate DATE NOT NULL,
  treatmenttype VARCHAR(300) NOT NULL,
  notes VARCHAR(300) NOT NULL,
  followupdate_ DATE NOT NULL,
  treatmenttime VARCHAR NOT NULL,
  doc_id INT NOT NULL,
  resident_id INT NOT NULL,
  PRIMARY KEY (treatmentdate, doc_id, resident_id),
  FOREIGN KEY (doc_id) REFERENCES doctors(doc_id),
  FOREIGN KEY (resident_id) REFERENCES residents(resident_id),
  UNIQUE (treatmenttime)
);

CREATE TABLE appointments
(
  appointmentdate DATE NOT NULL,
  purpose VARCHAR(100) NOT NULL,
  status VARCHAR(100) NOT NULL,
  appointmenttime VARCHAR(100) NOT NULL,
  resident_id INT NOT NULL,
  Doc_id INT NOT NULL,
  PRIMARY KEY (appointmentdate, resident_id, doc_id),
  FOREIGN KEY (resident_id) REFERENCES residents(resident_id),
  FOREIGN KEY (doc_id) REFERENCES doctors(doc_id),
  UNIQUE (appointmenttime)
);

CREATE TABLE residentmedications
(
  residentmedication_id INT NOT NULL,
  s_date DATE NOT NULL,
  e_date DATE NOT NULL,
  frequency VARCHAR(30) NOT NULL,
  prescribedby INT NOT NULL,
  resident_id INT NOT NULL,
  medication_id INT NOT NULL,
  PRIMARY KEY (residentmedication_id),
  FOREIGN KEY (resident_id) REFERENCES residents(resident_id),
  FOREIGN KEY (medication_id) REFERENCES medications(medication_id),
  UNIQUE (resident_id, medication_id)
);
