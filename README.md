# Nursing Home - Medicine

## Aharon Raanan & Levi Greenfeld

The system stores data on residents, doctors, medications, and the relationships between them:
- Doctor visits
- Treatments
- Medications that each resident should take (if needed)
- And more.

---

## [ERD (Entity-Relationship Diagram)](#erd-entity-relationship-diagram)
![ERD Diagram](https://github.com/user-attachments/assets/acc81ce9-0dc0-4119-91be-6d738da6b901)

---

## [DSD (Data Structure Diagram)](#dsd-data-structure-diagram)
![DSD Diagram](https://github.com/user-attachments/assets/31011c74-5903-494f-af79-15b81a33ffdc)

---

## [Tools Used for CSV File Creation](#tools-used-for-csv-file-creation)

### [First Tool: Using `generatedata` to Create CSV File](#first-tool-using-generatedata-to-create-csv-file)
![First Tool Screenshot](https://github.com/user-attachments/assets/9183710c-c128-407f-a34d-d4841d5468b4)

### [Second Tool: Using `mockaroo` to Create CSV File](#second-tool-using-mockaroo-to-create-csv-file)
![Second Tool Screenshot](https://github.com/user-attachments/assets/09e531f6-3ffb-4ec1-b9eb-353b4b0cd6d1)

### [Third Tool: Using Python to Create CSV File](#third-tool-using-python-to-create-csv-file)
![Third Tool Screenshot](https://github.com/user-attachments/assets/33415e6a-55d4-43ce-b872-cf293b1ba71c)

---

## [Photo of the Backup & Photo of the Restoration](#photo-of-the-backup--photo-of-the-restoration)

### Photo 1
![Backup Photo 1](https://github.com/user-attachments/assets/50152aa5-8198-4e0a-bfb9-db61b51e7687)

### Photo 2
![Backup Photo 2](https://github.com/user-attachments/assets/6c3f8a90-7d2f-4894-91c3-65f5e32fadfe)

### Photo 3
![Backup Photo 3](https://github.com/user-attachments/assets/c93697a1-8375-4bc6-931d-0b30109332c7)

### Photo 4
![Backup Photo 4](https://github.com/user-attachments/assets/febfa1c5-9cf8-43ff-8ee4-5e469d613faa)

### Photo 5
![Backup Photo 5](https://github.com/user-attachments/assets/7e628ba9-15f6-4a85-8efd-e7284f1b8d34)

---

## [Stage B: Select Queries](#stage-b-select-queries)

### [Query 1: Residents with More Than 4 Devices Borrowed, and the Number of Devices Borrowed](#query-1-residents-with-more-than-4-devices-borrowed-and-the-number-of-devices-borrowed)
![Select Query 1](https://github.com/user-attachments/assets/0bba89cf-8583-4faf-ae84-134e0bc5dc9b)

### [Query 2: The Most Borrowed Device and the Number of Its Borrowings](#query-2-the-most-borrowed-device-and-the-number-of-its-borrowings)
![Select Query 2](https://github.com/user-attachments/assets/e82c475c-5854-47fb-9619-7439af7c7226)

### [Query 3: The Number of Devices Borrowed Per Type, Sorted by Quantity](#query-3-the-number-of-devices-borrowed-per-type-sorted-by-quantity)
![Select Query 3](https://github.com/user-attachments/assets/a37eb3a9-9c3b-4b63-9396-37aa850097e7)

### [Query 4: Doctors Who Made the Most Visits](#query-4-doctors-who-made-the-most-visits)
![Select Query 4](https://github.com/user-attachments/assets/3a1a63ad-f3e6-4d21-a5ab-4536356f928d)

### [Query 5: Number of Visits and Devices Used Per Year](#query-5-number-of-visits-and-devices-used-per-year)
![Select Query 5](https://github.com/user-attachments/assets/f7caf71d-9ec0-496c-96ec-95fc58776cb8)

### [Query 6: Number of Medications Each Resident Takes](#query-6-number-of-medications-each-resident-takes)
![Select Query 6](https://github.com/user-attachments/assets/7160d26a-4508-4f69-b46c-0b89f4d6e354)

### [Query 7: All Details About the Oldest Resident](#query-7-all-details-about-the-oldest-resident)
![Select Query 7](https://github.com/user-attachments/assets/b3a2cec1-2fa2-4d2f-8d20-f54b47809a43)

### [Query 8: All Details About Patients and Their Visits](#query-8-all-details-about-patients-and-their-visits)
![Select Query 8](https://github.com/user-attachments/assets/4bb12c95-2fb2-4317-93de-c8428c385f34)

---

## [Update SQL Statements](#update-sql-statements)

### [Update 1: Checking and Updating Drug Expiry Date](#update-1-checking-and-updating-drug-expiry-date)
![Update 1](https://github.com/user-attachments/assets/3ebf7aa4-05ef-4b50-a321-ccd0badfeec4)
![Update 2](https://github.com/user-attachments/assets/48e2a19f-d36e-4d14-a360-5ffec8056c82)
![Update 3](https://github.com/user-attachments/assets/d2f8cb1c-35c4-439e-82d6-d5253c1e8511)

### [Update 2: Moving `purpose` and `status` from `appointment` to `medicaltreatments`](#update-2-moving-purpose-and-status-from-appointment-to-medicaltreatments)
![Update 4](https://github.com/user-attachments/assets/8d6e0006-38d1-423f-802f-0ea963d50f27)
![Update 5](https://github.com/user-attachments/assets/745ac4db-2d47-4dcc-a750-176ca5e5e3a4)
![Update 6](https://github.com/user-attachments/assets/83301915-50f3-4684-9da6-7de5e425b8d1)
![Update 7](https://github.com/user-attachments/assets/a978e881-a8f5-4aa6-a05c-b030bd06d32f)

### [Update 3: Updating `purpose` and `status` Based on Doctor's Specialty and Resident's Status](#update-3-updating-purpose-and-status-based-on-doctors-specialty-and-residents-status)
![Update 8](https://github.com/user-attachments/assets/4c451012-decb-4b5b-a603-beb6a50bd1fe)
![Update 9](https://github.com/user-attachments/assets/d63f6b29-2832-4863-baf0-1d95229e22c1)
![Update 10](https://github.com/user-attachments/assets/661d1e35-fbd0-4c0a-bda8-c2830779e7ee)
![Update 11](https://github.com/user-attachments/assets/a04e8fa2-f529-43f7-bc2d-909815df991e)

---

## [Delete SQL Statements](#delete-sql-statements)

### [Delete 1: Merging `appointment` with `medicaltreatments` and Dropping the `appointment` Table](#delete-1-merging-appointment-with-medicaltreatments-and-dropping-the-appointment-table)
![Delete 1](https://github.com/user-attachments/assets/28245ec1-6988-4a7c-9bd8-0832ff32193f)
![Delete 2](https://github.com/user-attachments/assets/945e83be-0a82-414d-a186-5a1545bf5e83)

### [Delete 2: Deleting Doctors with 'Dermatology' Specialty](#delete-2-deleting-doctors-with-dermatology-specialty)
![Delete 3](https://github.com/user-attachments/assets/a98fca7f-ac68-4e79-90e5-72b082d4f61a)
![Delete 4](https://github.com/user-attachments/assets/dc342fa9-5e04-480e-952a-f86727002bff)
![Delete 5](https://github.com/user-attachments/assets/95083717-54eb-4c36-b237-b34175c1d4db)

### [Delete 3: Deleting a Specific Resident Based on `resident_id`](#delete-3-deleting-a-specific-resident-based-on-resident_id)
![Delete 6](https://github.com/user-attachments/assets/7dbbc544-ec26-4e1f-8195-fca0a50507a2)
![Delete 7](https://github.com/user-attachments/assets/74b09d1b-0ccb-4cf2-af7e-4d18cbd5cb1f)

---

## [Constraints SQL Statements](#constraints-sql-statements)

### [Constraint 1: Ensuring First and Last Name for Doctors](#constraint-1-ensuring-first-and-last-name-for-doctors)
![Constraint 1](https://github.com/user-attachments/assets/b8dcd380-314b-4dd4-b9c7-99ea19214942)

### [Constraint 2: Setting Default Gender for Residents](#constraint-2-setting-default-gender-for-residents)
![Constraint 2](https://github.com/user-attachments/assets/b7f67951-7754-480c-bcab-75e9e1ba7518)
![Constraint 3](https://github.com/user-attachments/assets/39b17469-1618-401f-9740-d67b89976af7)

### [Constraint 3: Checking Medication Form Types](#constraint-3-checking-medication-form-types)
![Constraint 4](https://github.com/user-attachments/assets/93a806ee-033f-47a7-bcb4-04e9396093a1)


# stage C:

## img of reversing of Human Resources Management backup

![DSD of newDataBase](https://github.com/user-attachments/assets/514c188a-da41-4ff2-af49-97459918d58f)
![ERD ofNewDataBase](https://github.com/user-attachments/assets/9a295b87-a1fb-4fae-ae46-d19b93e47e6d)

## integrate Medicine and Human Resources Management schemas:
![intergrateERD](https://github.com/user-attachments/assets/5e477de8-21fc-41be-b44b-5a18089ca5b3)
![integrateDSD](https://github.com/user-attachments/assets/4d420469-98aa-4fbe-a7ea-5ba6316f3b2a)

## Integration Report:
During the integration performed in the database schema, several changes were made to existing tables, while maintaining the relationships between them and ensuring data upgrades in an organized manner. Here's a summary of the steps taken:

### 1. Decision that "Doctors" Inherit from "Employees"
It was decided that the doctors table would inherit its attributes from the employee table. This means that every doctor will also be considered an employee. The unique identifier employeeid_ is retained in the doctors table as a foreign key, and the doctors' data will be shared with the rest of the employees.

### 2. Changes in the doctors Table
After the decision that doctors are inherited entities, the attributes doc_gender, email, phone, and licenserenewaldate_ were retained in the doctors table.

All other attributes (such as doc_fname, doc_lname, specialization, hiredate) were moved to the employee table.

### Relationships Between Tables:
one-to-many relationships were established between medicalequipmentreceiving and doctors and residents:

The relationship between medicalequipmentreceiving and doctors:

medicalequipmentreceiving holds a foreign key pointing to employeeid_ in doctors. This means each row in the medicalequipmentreceiving table refers to a doctor (a foreign key pointing to doctors).

The relationship between medicalequipmentreceiving and residents:

medicalequipmentreceiving holds a foreign key pointing to resident_id in residents. This means each row in this table refers to a resident receiving the medical equipment.

### 3. Schema Changes
Throughout the integration, table names ending with an underscore (e.g., employee_, department_) were renamed to standardized names without the underscore to improve readability and create a consistent data structure.

For example: department_ was renamed to department.

### 4. Adding the "Medicine" Department
A new department, Medicine, was added to the database:

A new row was inserted into the department table with ID 504 and the email medicine@company.com.

### 5. Adding Rows to the position Table
Changes were made to the position table, which now includes job positions for doctors:

1000 rows were added with positionid_ ranging from 501 to 1500.

title_ was populated with the specializations from the doctors table (the doctor's specialization was transferred to title_).

A random salary was generated between 30000 and 150000.

All positions were assigned to the Medicine department with departmentid_ set to 504.

### 6. Adding Rows to the employee Table
1000 rows were added to the employee table for the doctors, with employeeid_ ranging from 1001 to 2000:

doc_fname and doc_lname were copied to firstname_ and lastname_ respectively.

hiredate from doctors was copied to hire_date in the employee table.

Additionally, active was set to true, and birthdate_ was initially set to 1970-01-01 (temporary date).

Added random birthdates between 1960 and 1998: Each new row in the employee table received a random birthdate within the specified range.

### 7. Updating the doctors Table
Changes were made to the doctors table:

The column doc_id was renamed to employeeid_, making it the foreign key pointing to the employee table.

The columns doc_fname, doc_lname, specialization, and hiredate were removed from the doctors table.

The employeeid_ column was updated in the range 1001 to 2000, ensuring that the doctor records in the doctors table align with the new values.

### 8. Removing Foreign Keys (Before Making Changes)
Before making the updates, foreign keys in the medicalequipmentreceiving and medicaltreatments tables were removed to avoid errors during the update:

The medicalequipmentreceiving table referenced employeeid_.

The medicaltreatments table also referenced employeeid_.

### 9. Updating Values in Dependent Tables
After updating the employeeid_ in the doctors table, the values in the employeeid_ columns of the medicalequipmentreceiving and medicaltreatments tables were updated by adding 1000 to each value:

All values in the employeeid_ column of the medicalequipmentreceiving table were updated to align with the new IDs in doctors.

All values in the doc_id column of the medicaltreatments table were updated to align with the new IDs in doctors.

### 10. Restoring Foreign Keys and Defining Primary Key
After updating the values in the doctors table, the foreign keys were restored:

doctors_employeeid_fkey: A foreign key pointing to employee.

doctors_pkey: A primary key on employeeid_ in the doctors table.

The foreign keys were also restored in the medicalequipmentreceiving and medicaltreatments tables.

### 11. Renaming the Column in medicaltreatments
Finally, the column doc_id in the medicaltreatments table was renamed to employeeid_, making it consistent with the new column name in the doctors table.
### View number 1
### View_residents
The view provides a comprehensive overview of residents' information, including personal details, recommended medical equipment, and medical treatments they have received. The view combines data from three tables: residents, medicalequipmentreceiving, and medicaltreatments, by joining them based on the resident's identifier (resident_id).
[![צילום מסך 2025-05-13 000718](https://github.com/user-attachments/assets/097c6119-ec7c-4532-b12f-c57683695644)](https://github.com/AharonRaanan/DBProject-318406014_315407403/blob/main/stage%20c/View%20residents.png)

[![צילום מסך 2025-05-13 000859](https://github.com/user-attachments/assets/ee24e403-4ebe-4a4f-8cda-993188b0827d)](https://github.com/AharonRaanan/DBProject-318406014_315407403/blob/main/stage%20c/select%20from%20view_residents.png)
### Query 1: Residents Who Received Medical Treatment but Were Not Recommended Medical Equipment

Objective: To identify residents who received medical treatment but were not recommended medical equipment, which may indicate the need for a reassessment of their needs.
[![צילום מסך 2025-05-13 002747](https://github.com/user-attachments/assets/c131c99f-1a1e-4e10-a34d-cdb3db36fffa)](https://github.com/AharonRaanan/DBProject-318406014_315407403/blob/main/stage%20c/View%20number%201%2C%20query-1.png)
### Query 2: Classifying Residents by the Type of Service They Received

Objective: To classify residents based on the type of service they received: medical treatment only, medical equipment only, both, or neither.

[![צילום מסך 2025-05-13 003501](https://github.com/user-attachments/assets/f1de009e-e8d9-45df-8e95-0f60ab67a9d6)](https://github.com/AharonRaanan/DBProject-318406014_315407403/blob/main/stage%20c/View%20number%201%2C%20query%202.png)
### View number 2
### View_employee
The view provides a comprehensive view of employee details along with information about any sanctions or bonuses assigned to them. It combines data from two tables: employee and sanctionbonus, using a FULL OUTER JOIN based on the employee ID (employeeid_ in the first table and recordid_ in the second).

[![View employee](https://raw.githubusercontent.com/AharonRaanan/DBProject-318406014_315407403/main/stage%20c/View%20employee.png)](https://github.com/AharonRaanan/DBProject-318406014_315407403/blob/main/stage%20c/View%20employee.png)

[![select from view employee](https://raw.githubusercontent.com/AharonRaanan/DBProject-318406014_315407403/main/stage%20c/select%20from%20view%20employee.png)](https://github.com/AharonRaanan/DBProject-318406014_315407403/blob/main/stage%20c/select%20from%20view%20employee.png)

### Query 1: Employees with the Highest Bonuses

Objective: To identify employees who have been assigned the highest bonuses, which may indicate exceptional performance.

[![View number 2, query 1](https://raw.githubusercontent.com/AharonRaanan/DBProject-318406014_315407403/main/stage%20c/View%20number%202%2C%20query%201.png)](https://github.com/AharonRaanan/DBProject-318406014_315407403/blob/main/stage%20c/View%20number%202%2C%20query%201.png)


### Query 2: Sanctions Assigned to Employees – By Frequency

Objective: To identify which sanctions have been assigned to employees most frequently, which may indicate recurring issues or the need for intervention.

[![View number 2, query 2](https://raw.githubusercontent.com/AharonRaanan/DBProject-318406014_315407403/main/stage%20c/View%20number%202%2C%20query%202.png)](https://github.com/AharonRaanan/DBProject-318406014_315407403/blob/main/stage%20c/View%20number%202%2C%20query%202.png)


# stage D:
## Function 1
### Function that returns positions with active employees count exceeding a given threshold
![צילום מסך 2025-06-17 191533](https://github.com/user-attachments/assets/0a010e36-cd2d-42e9-aead-7e43711ac99a)


![צילום מסך 2025-06-17 191350](https://github.com/user-attachments/assets/74bd24ad-1532-47a3-9f28-1f8da994ec7c)

![צילום מסך 2025-06-17 191442](https://github.com/user-attachments/assets/f637aeea-8b03-45c0-83e0-6767d619f21c)

## Function 2
### Function that returns active employees for a given position ID

![צילום מסך 2025-06-17 192212](https://github.com/user-attachments/assets/5f0ac17f-d323-4aa3-b35d-6a947e34defe)


![צילום מסך 2025-06-17 192252](https://github.com/user-attachments/assets/2cd9be6d-3fef-46f5-b538-be0c4501f282)


![צילום מסך 2025-06-17 192259](https://github.com/user-attachments/assets/f749de4d-9c37-4805-b9be-400ea4fdd2f0)

## Function 3
### Function that summarizes equipment usage by residents filtered by various criteria

![צילום מסך 2025-06-17 192629](https://github.com/user-attachments/assets/7cc2db28-aebc-4c42-9b8d-6d5d40be2dab)

![צילום מסך 2025-06-17 192647](https://github.com/user-attachments/assets/a5d4f1b1-9364-44ff-aae1-0e2e5553fa25)

![צילום מסך 2025-06-17 192703](https://github.com/user-attachments/assets/156ade71-507f-4df4-89a2-6cefae333ab8)

![צילום מסך 2025-06-17 193029](https://github.com/user-attachments/assets/5f16d5e0-2be8-4257-99e4-317f22211f51)

![צילום מסך 2025-06-17 193043](https://github.com/user-attachments/assets/244a238a-d75d-42bb-a191-0358d3c47867)

## Procedure 1
### Procedure that updates doctors' email addresses based on their first names matched from employee records

![צילום מסך 2025-06-17 193420](https://github.com/user-attachments/assets/cb7f6af4-c57c-40a0-98e3-8371db7db5ed)

![צילום מסך 2025-06-17 193456](https://github.com/user-attachments/assets/600a47f4-ac24-4e5e-aa1b-39b6cbd1f43b)
## Procedure 2
### Procedure that updates medication status for residents based on cutoff date and logs the changes

![צילום מסך 2025-06-17 193622](https://github.com/user-attachments/assets/21ddf00c-f781-4b9c-ac06-1c556b39cd1e)


![צילום מסך 2025-06-17 193725](https://github.com/user-attachments/assets/bb613451-ec86-4ed1-b55b-d9d286a05892)
## Trigger 1
### Trigger that logs changes when a doctor's email or phone number is updated

![צילום מסך 2025-06-17 193928](https://github.com/user-attachments/assets/c50fdb2f-91f0-4c13-bd57-0b0c25c384d5)

![צילום מסך 2025-06-17 194029](https://github.com/user-attachments/assets/5e611871-602c-45ca-8114-597154c8206e)
## Trigger 2
### Trigger that logs every new insert into the sanctionbonus table

![צילום מסך 2025-06-17 194234](https://github.com/user-attachments/assets/391fcbf8-0dde-4aa8-93e8-d140d00e6e13)


![צילום מסך 2025-06-17 194254](https://github.com/user-attachments/assets/28e2ba30-bc03-4b5f-a388-e61649ef940d)

## Main 1
![צילום מסך 2025-06-17 194952](https://github.com/user-attachments/assets/d6a3cce5-5b65-4cec-ad8a-55e77993c8f3)
![צילום מסך 2025-06-17 194952](https://github.com/user-attachments/assets/d6a3cce5-5b65-4cec-ad8a-55e77993c8f3)

## Main 2

![צילום מסך 2025-06-17 195009](https://github.com/user-attachments/assets/f32ef5d7-7e53-4a49-a69e-05b76b854c27)
![צילום מסך 2025-06-17 195009](https://github.com/user-attachments/assets/f32ef5d7-7e53-4a49-a69e-05b76b854c27)


# stage E:


# 🏥 Enhanced Database Management System – Version 5.1

**Developed by:** Aharon Raanan & Levi Yitzchak Grinfeld  
**Year:** 2025

A full-featured PostgreSQL-based desktop system for managing elderly care facilities, supporting CRUD operations, visual queries, functions, and procedures – all through a modern GUI built with Python and Tkinter.

---

## 📥 Login Screen

To start using the system:

- **Username:** Your PostgreSQL username (same as in pgAdmin4)
- **Password:** Your database user's password
- **Host:** Use `localhost` (or another host if remote)
- **Database:** Name of the database you want to connect to

➡️ Click **`Connect to Database`** to access the main dashboard.

---

## 🧭 Main Interface (Tabs Overview)

Once connected, the interface displays multiple tabs:

- `Residents`, `Doctors`, `Medications`, `Employees`, `Equipment`, `Treatments`, `Departments`, `Positions`
- Additional tabs: `Queries & Reports`, `Functions`, `Procedures`

Each data tab includes:
- ✅ **Add Record**
- ✏️ **Edit Record**
- ❌ **Delete Record**
- 🔄 **Refresh**
- 📤 **Export**
- 🔍 **Search bar** for filtering

---

## 📁 File Menu (Top Left)

The `File` menu includes:

- 🔒 **Logout** – Return to the login screen (switch user/database)
- ❌ **Exit** – Close the application

Accessible from all screens.

---

## 🛠️ Functions Tab

Execute stored PostgreSQL functions with optional parameters:

1. Click **`Refresh Functions`**
2. Select a function
3. Input parameters (if needed)
4. Click **`Run Function`**
5. View output in the result area

📌 Example functions:
- `count_active_employees_by_position(position_id)`
- `get_equipment_residents_summary(min_devices, min_rentals, min_current_rentals)`

---

## ⚙️ Procedures Tab

Run stored procedures with or without parameters:

1. Click **`Refresh Procedures`**
2. Select a procedure
3. Provide parameters if required
4. Click **`Run Procedure`**
5. Output or success message will be shown below

📌 Example procedures:
- `update_doctors_email_by_firstname()`
- `update_resident_medication_status(cutoff_date)`

---

## 📊 Queries & Reports Tab

Visualize and explore advanced queries:

1. Select a query from the dropdown
2. Click **`Run Query`**
3. See results in a formatted text table
4. View automatic **visual charts** below (Bar, Pie, or Line)

📌 Example query:
> **Residents with more than 4 devices**

---

## ℹ️ About Screen (via `Help` Menu)

Navigate to `Help > About` to view:

- System version and year
- Developer credits
- Feature highlights
- Listed available:
  - Functions
  - Procedures
- Enhanced version 5.1 capabilities

---

## 🌟 Enhanced Features (v5.1)

- Parameter input detection for functions and procedures
- Automatic parameter type conversion
- Custom input dialogs
- Filtered display (custom objects only)
- Real-time schema monitoring
- Export functionality (CSV)
- Advanced query visualizations:
  - Bar Charts
  - Pie Charts
  - Line Charts
- Detailed error handling with rollback support

---

© 2025 All rights reserved

## 🧰 Development Tools & Workflow

This system was developed as part of an academic database project, with the goal of creating a user-friendly desktop interface for managing and interacting with a PostgreSQL database.

---

### 🧠 AI Assistance

To accelerate development and ensure best practices, we actively used:
- **ChatGPT (OpenAI)** – for architectural advice, code generation, bug fixing, and user interface ideas
- **Claude (Anthropic)** – for additional insights, natural language clarification, and code explanations

The final product reflects a combination of human logic and AI-enhanced programming.

---

### 🖥️ Programming Language

- **Python 3.11** – used for its simplicity and powerful ecosystem
- The entire application is implemented in a single, modular Python file for maximum portability

---

### 🪟 GUI Framework

- **Tkinter** – used to build all application windows, forms, and widgets
- **ttk** – used for advanced widgets like tabbed views (`Notebook`) and tables (`Treeview`)

---

### 🗄️ Database System

- **PostgreSQL** – used as the central database engine
- **pgAdmin 4** – used for schema design, function/procedure creation, and manual testing

The system connects directly to a PostgreSQL server using user-provided credentials and database name.

---

### 🔌 Database Connectivity

- **psycopg2-binary** is used to:
  - Establish and manage database connections
  - Execute **SQL queries**, **stored procedures**, and **functions**
  - Handle parameterized inputs and transaction rollback

---

### 📊 Visualization

- **Matplotlib** – integrated with Tkinter for graphing:
  - Bar charts
  - Pie charts
  - Line charts

These are automatically displayed based on query results.

---

### 🧠 Application Logic

The system supports full **bidirectional interaction** with the database:

- ✅ **Read**: fetch data from PostgreSQL and display it in interactive tables
- ✅ **Write**: add/edit/delete records that are saved back to the database
- ✅ **Run**: call stored **functions** and **procedures** from PostgreSQL with dynamic parameter input
- ✅ **Visualize**: convert SQL query results into real-time charts

All changes are immediately reflected in the database using SQL `INSERT`, `UPDATE`, `DELETE`, and `CALL`.

---



### Username: myuser
### Password: mypassword

![צילום מסך 2025-06-24 193358](https://github.com/user-attachments/assets/9aaf9b37-86c2-4ffd-8d47-07eac5931eca)


## The data

![צילום מסך 2025-06-24 190759](https://github.com/user-attachments/assets/0b4224b3-8edf-400f-81de-6a3316f167f3)
## Example of query 1
![צילום מסך 2025-06-24 191416](https://github.com/user-attachments/assets/4cead5c2-6c6c-4f80-a717-b7672634b842)

## Example of query 2
![צילום מסך 2025-06-24 191433](https://github.com/user-attachments/assets/993c8b2e-98eb-478b-a20c-dca0482a0721)

## Example of Function 1

![צילום מסך 2025-06-24 190917](https://github.com/user-attachments/assets/922dfc66-7a87-4a26-8256-df35b1a5b78d)
## Example of Function 2
![צילום מסך 2025-06-24 190957](https://github.com/user-attachments/assets/64815a69-60ca-46ec-8d8a-14fb04d84ef2)

## Example of Procedure 1
![צילום מסך 2025-06-24 191011](https://github.com/user-attachments/assets/bbcf42ab-77e2-40ea-a29a-b61824f76657)

## Example of Procedure 2

![צילום מסך 2025-06-24 191047](https://github.com/user-attachments/assets/ef40b934-ad2a-4492-9282-d9e255845387)


