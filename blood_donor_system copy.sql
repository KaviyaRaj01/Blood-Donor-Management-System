-- Blood Donor Reservation System Database Setup

-- Blood Donor Reservation System Database Setup

-- 1. Drop Existing Tables (if needed, for fresh setup)
DROP TABLE Reservations CASCADE CONSTRAINTS;
DROP TABLE Donors CASCADE CONSTRAINTS;
DROP TABLE Blood_Types CASCADE CONSTRAINTS;

-- 2. Create Tables
CREATE TABLE Blood_Types (
    blood_type_id NUMBER PRIMARY KEY,
    blood_type VARCHAR2(5) NOT NULL UNIQUE,
    available_units NUMBER DEFAULT 0 CHECK (available_units >= 0)  -- Ensure units cannot be negative
);

CREATE TABLE Donors (
    donor_id NUMBER PRIMARY KEY,
    name VARCHAR2(50) NOT NULL,
    age NUMBER(3) CHECK (age >= 18 AND age <= 65),
    contact_number VARCHAR2(15) UNIQUE NOT NULL,
    blood_type_id NUMBER,
    document BLOB,
    FOREIGN KEY (blood_type_id) REFERENCES Blood_Types(blood_type_id) ON DELETE SET NULL -- This allows deletion of blood types without orphaning donors
);

CREATE TABLE Reservations (
    reservation_id NUMBER PRIMARY KEY,
    donor_id NUMBER,
    reservation_date DATE DEFAULT SYSDATE,
    reservation_time VARCHAR2(10),
    status VARCHAR2(20) CHECK (status IN ('Scheduled', 'Completed', 'Canceled')),
    FOREIGN KEY (donor_id) REFERENCES Donors(donor_id) ON DELETE CASCADE -- Deleting a donor will remove their reservations
);


-- 4. Create Triggers
-- Trigger for Updating Blood Units
CREATE OR REPLACE TRIGGER update_blood_units
AFTER UPDATE OF status ON Reservations
FOR EACH ROW
WHEN (NEW.status = 'Completed')
BEGIN
    DECLARE v_blood_type_id NUMBER;
    BEGIN
        SELECT blood_type_id INTO v_blood_type_id FROM Donors WHERE donor_id = :NEW.donor_id;
        UPDATE Blood_Types SET available_units = available_units + 1 WHERE blood_type_id = v_blood_type_id;
    END;
END;
/

-- 5. Create Stored Procedures and Functions
-- Procedure to Add Donor
CREATE OR REPLACE PROCEDURE add_donor (
    p_name IN VARCHAR2,
    p_age IN NUMBER,
    p_contact_number IN VARCHAR2,
    p_blood_type_id IN NUMBER,
    p_document IN BLOB
) AS
BEGIN
    INSERT INTO Donors (donor_id, name, age, contact_number, blood_type_id, document)
    VALUES ((SELECT NVL(MAX(donor_id), 0) + 1 FROM Donors), p_name, p_age, p_contact_number, p_blood_type_id, p_document);
END add_donor;
/

-- Function to Check Blood Availability
CREATE OR REPLACE FUNCTION check_blood_availability(p_blood_type_id IN NUMBER)
RETURN NUMBER AS
    v_available_units NUMBER;
BEGIN
    SELECT available_units INTO v_available_units FROM Blood_Types WHERE blood_type_id = p_blood_type_id;
    RETURN v_available_units;
END check_blood_availability;

-- Procedure to Book Reservation
CREATE OR REPLACE PROCEDURE book_reservation (
    p_donor_id IN NUMBER,
    p_reservation_time IN VARCHAR2,
    p_status IN VARCHAR2
) AS
BEGIN
    DECLARE
        v_blood_type_id NUMBER;
        v_available_units NUMBER;
    BEGIN
        SELECT blood_type_id INTO v_blood_type_id FROM Donors WHERE donor_id = p_donor_id;
        v_available_units := check_blood_availability(v_blood_type_id);
        IF v_available_units <= 0 THEN
            RAISE_APPLICATION_ERROR(-20002, 'Insufficient blood units available.');
        END IF;

        INSERT INTO Reservations (reservation_id, donor_id, reservation_date, reservation_time, status)
        VALUES ((SELECT NVL(MAX(reservation_id), 0) + 1 FROM Reservations), p_donor_id, SYSDATE, p_reservation_time, p_status);
    END;
    
END book_reservation;
/

-- 6. Insert Sample Data (optional, for testing)
INSERT INTO Blood_Types (blood_type_id, blood_type, available_units) VALUES (1, 'A+', 10);
INSERT INTO Blood_Types (blood_type_id, blood_type, available_units) VALUES (2, 'A-', 5);
INSERT INTO Blood_Types (blood_type_id, blood_type, available_units) VALUES (3, 'B+', 8);
INSERT INTO Blood_Types (blood_type_id, blood_type, available_units) VALUES (4, 'B-', 4);
INSERT INTO Blood_Types (blood_type_id, blood_type, available_units) VALUES (5, 'O+', 15);
INSERT INTO Blood_Types (blood_type_id, blood_type, available_units) VALUES (6, 'O-', 3);
INSERT INTO Blood_Types (blood_type_id, blood_type, available_units) VALUES (7, 'AB+', 7);
INSERT INTO Blood_Types (blood_type_id, blood_type, available_units) VALUES (8, 'AB-', 2);

INSERT INTO Donors (donor_id, name, age, contact_number, blood_type_id) VALUES (101, 'Alice Smith', 30, '1234567890', 1);
INSERT INTO Donors (donor_id, name, age, contact_number, blood_type_id) VALUES (102, 'Bob Johnson', 45, '0987654321', 2);
INSERT INTO Donors (donor_id, name, age, contact_number, blood_type_id) VALUES (103, 'Catherine Lee', 29, '1122334455', 3);
INSERT INTO Donors (donor_id, name, age, contact_number, blood_type_id) VALUES (104, 'David Brown', 36, '2233445566', 4);
INSERT INTO Donors (donor_id, name, age, contact_number, blood_type_id) VALUES (105, 'Eva Williams', 25, '3344556677', 5);


INSERT INTO Reservations (reservation_id, donor_id, reservation_date, reservation_time, status) VALUES (201, 101, TO_DATE('2024-12-01', 'YYYY-MM-DD'), '10:00', 'Scheduled');
INSERT INTO Reservations (reservation_id, donor_id, reservation_date, reservation_time, status) VALUES (202, 102, TO_DATE('2024-12-02', 'YYYY-MM-DD'), '11:00', 'Scheduled');
INSERT INTO Reservations (reservation_id, donor_id, reservation_date, reservation_time, status) VALUES (203, 103, TO_DATE('2024-12-03', 'YYYY-MM-DD'), '09:00', 'Scheduled');
INSERT INTO Reservations (reservation_id, donor_id, reservation_date, reservation_time, status) VALUES (204, 104, TO_DATE('2024-12-04', 'YYYY-MM-DD'), '14:00', 'Scheduled');
INSERT INTO Reservations (reservation_id, donor_id, reservation_date, reservation_time, status) VALUES (205, 105, TO_DATE('2024-12-05', 'YYYY-MM-DD'), '16:00', 'Scheduled');

commit;