-- Adding a NOT NULL constraint to the 'doc_fname' and 'doc_lname' columns in the 'doctors' table
ALTER TABLE public.doctors
    ALTER COLUMN doc_fname SET NOT NULL,
    ALTER COLUMN doc_lname SET NOT NULL;


-- Adding a DEFAULT value for 'r_gender' column in the 'residents' table to default to 'Unknown'
ALTER TABLE public.residents
    ALTER COLUMN r_gender SET DEFAULT 'Unknown';

ALTER TABLE public.medications
    ADD CONSTRAINT form_check CHECK (form IN ('Oral', 'Topical', 'Intramuscular', 'Intravenous', 'Subcutaneous', 'Intranasal'));

	
	






