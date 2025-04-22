Aharon Raanan & Levi Greenfeld

Nursing home - medicine

The system stores data on residents, doctors, medications, and the relationships between them
Doctor visits, treatments, medications that each resident should take (if needed),
and more.


ERD (Entity-Relationship Diagram)
  ![PHOTO-2025-04-01-13-48-06](https://github.com/user-attachments/assets/acc81ce9-0dc0-4119-91be-6d738da6b901)
  
DSD (Data Structure Diagram)
![PHOTO-2025-04-01-13-48-38](https://github.com/user-attachments/assets/31011c74-5903-494f-af79-15b81a33ffdc)


First tool: using generatedata. to create csv file

![צילום מסך 2025-04-01 152519](https://github.com/user-attachments/assets/9183710c-c128-407f-a34d-d4841d5468b4)


Second tool: using mockaro to create csv file
![צילום מסך 2025-04-01 161613](https://github.com/user-attachments/assets/09e531f6-3ffb-4ec1-b9eb-353b4b0cd6d1)



Third tool: using python to create csv file
![83FAE20A-6067-40D2-9430-159B9E7FBA4F](https://github.com/user-attachments/assets/33415e6a-55d4-43ce-b872-cf293b1ba71c)

Photo of the backup & Photo of the restoration

![PHOTO-2025-04-01-18-40-23](https://github.com/user-attachments/assets/50152aa5-8198-4e0a-bfb9-db61b51e7687)

![PHOTO-2025-04-01-18-45-46](https://github.com/user-attachments/assets/6c3f8a90-7d2f-4894-91c3-65f5e32fadfe)

![PHOTO-2025-04-01-19-03-37](https://github.com/user-attachments/assets/c93697a1-8375-4bc6-931d-0b30109332c7)

![PHOTO-2025-04-01-19-04-43](https://github.com/user-attachments/assets/febfa1c5-9cf8-43ff-8ee4-5e469d613faa)

![PHOTO-2025-04-01-19-05-50](https://github.com/user-attachments/assets/7e628ba9-15f6-4a85-8efd-e7284f1b8d34)

Aharon Raanan & Levi Greenfeld

Stage B:

Select queries:


פרטי הדיירים שיש להם יותר מ-4 מכשירים מושאלים, וכמות המכשירים שמושאלים אצלם:
![צילום מסך 2025-04-22 202625](https://github.com/user-attachments/assets/18224ae2-0700-4fe4-a051-558648f65d6a)


מציאת המכשיר שמושאל הכי הרבה, וכמות ההשאלות שלו:
![צילום מסך 2025-04-22 202757](https://github.com/user-attachments/assets/e82c475c-5854-47fb-9619-7439af7c7226)


כמות המכשירים שמושאלים כרגע מכל סוג, ממוין לפי כמות:
![צילום מסך 2025-04-22 202833](https://github.com/user-attachments/assets/a37eb3a9-9c3b-4b63-9396-37aa850097e7)


שמות הרופאים שביצעו הכי הרבה ביקורים:
![צילום מסך 2025-04-22 202917](https://github.com/user-attachments/assets/3a1a63ad-f3e6-4d21-a5ab-4536356f928d)


כמות הביקורים וכמות המכשירים שהיו בשימוש לפי שנים:
![צילום מסך 2025-04-22 203002](https://github.com/user-attachments/assets/f7caf71d-9ec0-496c-96ec-95fc58776cb8)


כמות התרופות שכל דייר לוקח:
![צילום מסך 2025-04-22 203036](https://github.com/user-attachments/assets/7160d26a-4508-4f69-b46c-0b89f4d6e354)


כל הפרטים על הדייר הכי מבוגר:
(ניתן להחליף את התנאי ולמצוא את כל הפרטים על כל דייר אחר שנבחר, בעזרת שאילתה זו)
![צילום מסך 2025-04-22 203127](https://github.com/user-attachments/assets/b3a2cec1-2fa2-4d2f-8d20-f54b47809a43)

פרטי כל מטופל והביקורים שהיו אצלו:
![צילום מסך 2025-04-22 203551](https://github.com/user-attachments/assets/4bb12c95-2fb2-4317-93de-c8428c385f34)


Update.sql:

1. 
אני בודק האם יש תאריכי הנפקת תרופה שהן מאוחרים מתאריך תוקף התרופה, מצאנו שיש. כדי לפתור את הקונפליקט כתבנו שאילתת update כך, שבכל נתון עם מצב כזה, השאילתא תחליף בין התאריכים כך שזה יהיה הגיוני.
![image](https://github.com/user-attachments/assets/3ebf7aa4-05ef-4b50-a321-ccd0badfeec4)
![image](https://github.com/user-attachments/assets/48e2a19f-d36e-4d14-a360-5ffec8056c82)
![image](https://github.com/user-attachments/assets/d2f8cb1c-35c4-439e-82d6-d5253c1e8511)

2.

אנו רוצים לקחת את המאפיינים purpos, status מטבלת appointment ולהעביר אותם לטבלת medicaltreatments 

![image](https://github.com/user-attachments/assets/8d6e0006-38d1-423f-802f-0ea963d50f27)
![image](https://github.com/user-attachments/assets/745ac4db-2d47-4dcc-a750-176ca5e5e3a4)
![image](https://github.com/user-attachments/assets/83301915-50f3-4684-9da6-7de5e425b8d1)
![image](https://github.com/user-attachments/assets/a978e881-a8f5-4aa6-a05c-b030bd06d32f)

3.
באמצעות שאילתת update אני רוצה לעדכן בטבלת medicaltreatments את המאפיין purpose לפי ההתמחות של הרופא ואת המאפיין status לפי הסטטוס של הדייר.
![image](https://github.com/user-attachments/assets/4c451012-decb-4b5b-a603-beb6a50bd1fe)
![image](https://github.com/user-attachments/assets/d63f6b29-2832-4863-baf0-1d95229e22c1)
![image](https://github.com/user-attachments/assets/661d1e35-fbd0-4c0a-bda8-c2830779e7ee)
![image](https://github.com/user-attachments/assets/a04e8fa2-f529-43f7-bc2d-909815df991e)

delete.sql:

1.

החלטנו לאחד את טבלת appointment עם הטבלה medicaltreatments, לכן אנחנו מוחקים את טבלת appointment.
![image](https://github.com/user-attachments/assets/28245ec1-6988-4a7c-9bd8-0832ff32193f)
![image](https://github.com/user-attachments/assets/945e83be-0a82-414d-a186-5a1545bf5e83)

2.

אנחנו מוחקים את כל הרופאים בטבלת doctors שהתמחותם היא 'dermatology
![image](https://github.com/user-attachments/assets/a98fca7f-ac68-4e79-90e5-72b082d4f61a)
![image](https://github.com/user-attachments/assets/dc342fa9-5e04-480e-952a-f86727002bff)
![image](https://github.com/user-attachments/assets/95083717-54eb-4c36-b237-b34175c1d4db)
אפשר לראות שחסר את רופא מספר 5 למשל

3.

בשאילתא זו אנחנו מוחקים דייר ספציפי בטבלת residents לפי resident_id.
![image](https://github.com/user-attachments/assets/7dbbc544-ec26-4e1f-8195-fca0a50507a2)
![image](https://github.com/user-attachments/assets/74b09d1b-0ccb-4cf2-af7e-4d18cbd5cb1f)


Constraints.sql:

1.
ALTER TABLE public.doctors
    ALTER COLUMN doc_fname SET NOT NULL,
    ALTER COLUMN doc_lname SET NOT NULL

    השאילתא נועדה לדאוג שלא יהיה אפשר למלא נתונים על רופא מבלי לציין את השם פרטי ומשפחה שלו:
  

  ![image](https://github.com/user-attachments/assets/b8dcd380-314b-4dd4-b9c7-99ea19214942)

2.
  ALTER TABLE public.residents
    ALTER COLUMN r_gender SET DEFAULT 'Unknown';

  השאילתא נועדה למקרה שאם לא מציינים את המין הדייר, אז ברירת המחדל הוא יהיה Unknown, אבל אם יכניסו כל ערך אחר שלא male/female/Non binary: אז תהיה שגיאה

  ![image](https://github.com/user-attachments/assets/b7f67951-7754-480c-bcab-75e9e1ba7518)

  ![image](https://github.com/user-attachments/assets/39b17469-1618-401f-9740-d67b89976af7)

3.
    ALTER TABLE public.medications
    ADD CONSTRAINT form_check CHECK (form IN ('Oral', 'Topical', 'Intramuscular', 'Intravenous', 'Subcutaneous', 'Intranasal'));

  
מטרת השאילתא לדאוג, שלא יכנסו ערכים אחרים מאלו שברשימה לעמודת form, אם יכנס ערך שלא ברשימה נקבל שגיאה:

![image](https://github.com/user-attachments/assets/93a806ee-033f-47a7-bcb4-04e9396093a1)

  
