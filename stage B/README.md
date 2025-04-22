Aharon Raanan & Levi Greenfeld

Stage B:

Select queries:


[DBProject-318406014_315407403/stage B
/Select__queries.docx](https://github.com/AharonRaanan/DBProject-318406014_315407403/blob/main/stage%20B/Select__queries.docx)

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

Constraints.sql:

1.
ALTER TABLE public.doctors
    ALTER COLUMN doc_fname SET NOT NULL,
    ALTER COLUMN doc_lname SET NOT NULL

    השאילתא נועדה לדאוג שאי אפשר למלא נתונים על רופא מבלי לציין את השם פרטי ומשפחה שלו:
  

    ![image](https://github.com/user-attachments/assets/b8dcd380-314b-4dd4-b9c7-99ea19214942)

3.
  ALTER TABLE public.residents
    ALTER COLUMN r_gender SET DEFAULT 'Unknown';

  השאילתא נועדה למקרה שאם לא מציינים את המין הדייר, אז ברירת המחדל הוא יהיה Unknown, אבל אם יכניסו כל ערך אחר שלא male/female/Non binary: אז תהיה שגיאה

  ![image](https://github.com/user-attachments/assets/b7f67951-7754-480c-bcab-75e9e1ba7518)

  ![image](https://github.com/user-attachments/assets/39b17469-1618-401f-9740-d67b89976af7)

4.
    ALTER TABLE public.medications
    ADD CONSTRAINT form_check CHECK (form IN ('Oral', 'Topical', 'Intramuscular', 'Intravenous', 'Subcutaneous', 'Intranasal'));

  
מטרת השאילתא לדאוג, שלא יכנסו ערכים אחרים מאלו שברשימה לעמודת form, אם יכנס ערך שלא ברשימה נקבל שגיאה:

![image](https://github.com/user-attachments/assets/93a806ee-033f-47a7-bcb4-04e9396093a1)

  
