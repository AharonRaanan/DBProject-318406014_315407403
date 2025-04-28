# Nursing Home - Medicine

## Aharon Raanan & Levi Greenfeld

The system stores data on residents, doctors, medications, and the relationships between them:
- Doctor visits
- Treatments
- Medications that each resident should take (if needed)
- And more.

---

## ERD (Entity-Relationship Diagram)
![ERD Diagram](https://github.com/user-attachments/assets/acc81ce9-0dc0-4119-91be-6d738da6b901)

---

## DSD (Data Structure Diagram)
![DSD Diagram](https://github.com/user-attachments/assets/31011c74-5903-494f-af79-15b81a33ffdc)

---

## Tools Used for CSV File Creation

### First tool: using `generatedata` to create csv file
![First Tool Screenshot](https://github.com/user-attachments/assets/9183710c-c128-407f-a34d-d4841d5468b4)

### Second tool: using `mockaroo` to create csv file
![Second Tool Screenshot](https://github.com/user-attachments/assets/09e531f6-3ffb-4ec1-b9eb-353b4b0cd6d1)

### Third tool: using Python to create csv file
![Third Tool Screenshot](https://github.com/user-attachments/assets/33415e6a-55d4-43ce-b872-cf293b1ba71c)

---

## Photo of the Backup & Photo of the Restoration

![Backup Photo 1](https://github.com/user-attachments/assets/50152aa5-8198-4e0a-bfb9-db61b51e7687)
![Backup Photo 2](https://github.com/user-attachments/assets/6c3f8a90-7d2f-4894-91c3-65f5e32fadfe)
![Backup Photo 3](https://github.com/user-attachments/assets/c93697a1-8375-4bc6-931d-0b30109332c7)
![Backup Photo 4](https://github.com/user-attachments/assets/febfa1c5-9cf8-43ff-8ee4-5e469d613faa)
![Backup Photo 5](https://github.com/user-attachments/assets/7e628ba9-15f6-4a85-8efd-e7284f1b8d34)

---

## Stage B: Select Queries

### Query 1: Residents with more than 4 devices borrowed, and the number of devices borrowed
![Select Query 1](https://github.com/user-attachments/assets/0bba89cf-8583-4faf-ae84-134e0bc5dc9b)

### Query 2: The most borrowed device and the number of its borrowings
![Select Query 2](https://github.com/user-attachments/assets/e82c475c-5854-47fb-9619-7439af7c7226)

### Query 3: The number of devices borrowed per type, sorted by quantity
![Select Query 3](https://github.com/user-attachments/assets/a37eb3a9-9c3b-4b63-9396-37aa850097e7)

### Query 4: Doctors who made the most visits
![Select Query 4](https://github.com/user-attachments/assets/3a1a63ad-f3e6-4d21-a5ab-4536356f928d)

### Query 5: Number of visits and devices used per year
![Select Query 5](https://github.com/user-attachments/assets/f7caf71d-9ec0-496c-96ec-95fc58776cb8)

### Query 6: Number of medications each resident takes
![Select Query 6](https://github.com/user-attachments/assets/7160d26a-4508-4f69-b46c-0b89f4d6e354)

### Query 7: All details about the oldest resident
![Select Query 7](https://github.com/user-attachments/assets/b3a2cec1-2fa2-4d2f-8d20-f54b47809a43)

### Query 8: All details about patients and their visits
![Select Query 8](https://github.com/user-attachments/assets/4bb12c95-2fb2-4317-93de-c8428c385f34)

---

## Update SQL Statements

### 1. Checking and Updating Drug Expiry Date
We check if there are drug issuance dates that are later than the drug's expiry date. We solve the conflict by using an update query to switch the dates for those records.
![Update 1](https://github.com/user-attachments/assets/3ebf7aa4-05ef-4b50-a321-ccd0badfeec4)
![Update 2](https://github.com/user-attachments/assets/48e2a19f-d36e-4d14-a360-5ffec8056c82)
![Update 3](https://github.com/user-attachments/assets/d2f8cb1c-35c4-439e-82d6-d5253c1e8511)

### 2. Moving `purpose` and `status` from `appointment` to `medicaltreatments`
![Update 4](https://github.com/user-attachments/assets/8d6e0006-38d1-423f-802f-0ea963d50f27)
![Update 5](https://github.com/user-attachments/assets/745ac4db-2d47-4dcc-a750-176ca5e5e3a4)
![Update 6](https://github.com/user-attachments/assets/83301915-50f3-4684-9da6-7de5e425b8d1)
![Update 7](https://github.com/user-attachments/assets/a978e881-a8f5-4aa6-a05c-b030bd06d32f)

### 3. Updating `purpose` and `status` Based on Doctor's Specialty and Resident's Status
![Update 8](https://github.com/user-attachments/assets/4c451012-decb-4b5b-a603-beb6a50bd1fe)
![Update 9](https://github.com/user-attachments/assets/d63f6b29-2832-4863-baf0-1d95229e22c1)
![Update 10](https://github.com/user-attachments/assets/661d1e35-fbd0-4c0a-bda8-c2830779e7ee)
![Update 11](https://github.com/user-attachments/assets/a04e8fa2-f529-43f7-bc2d-909815df991e)

---

## Delete SQL Statements

### 1. Merging `appointment` with `medicaltreatments` and Dropping the `appointment` Table
![Delete 1](https://github.com/user-attachments/assets/28245ec1-6988-4a7c-9bd8-0832ff32193f)
![Delete 2](https://github.com/user-attachments/assets/945e83be-0a82-414d-a186-5a1545bf5e83)

### 2. Deleting Doctors with 'Dermatology' Specialty
![Delete 3](https://github.com/user-attachments/assets/a98fca7f-ac68-4e79-90e5-72b082d4f61a)
![Delete 4](https://github.com/user-attachments/assets/dc342fa9-5e04-480e-952a-f86727002bff)
![Delete 5](https://github.com/user-attachments/assets/95083717-54eb-4c36-b237-b34175c1d4db)

### 3. Deleting a Specific Resident Based on `resident_id`
![Delete 6](https://github.com/user-attachments/assets/7dbbc544-ec26-4e1f-8195-fca0a50507a2)
![Delete 7](https://github.com/user-attachments/assets/74b09d1b-0ccb-4cf2-af7e-4d18cbd5cb1f)

---

## Constraints SQL Statements

### 1. Ensuring First and Last Name for Doctors
This constraint ensures that doctors must have both a first and last name specified.
![Constraint 1](https://github.com/user-attachments/assets/b8dcd380-314b-4dd4-b9c7-99ea19214942)

### 2. Setting Default Gender for Residents
If no gender is specified, the default is set to 'Unknown'. Invalid values will result in an error.
![Constraint 2](https://github.com/user-attachments/assets/b7f67951-7754-480c-bcab-75e9e1ba7518)
![Constraint 3](https://github.com/user-attachments/assets/39b17469-1618-401f-9740-d67b89976af7)

### 3. Checking Medication Form Types
This constraint ensures only valid medication forms are entered.
![Constraint 4](https://github.com/user-attachments/assets/93a806ee-033f-47a7-bcb4-04e9396093a1)
