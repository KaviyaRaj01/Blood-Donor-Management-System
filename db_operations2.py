import oracledb

# Establish a connection to the Oracle database
connection = oracledb.connect(
    user="system",
    password="kaviya1510",
    dsn="localhost:1522/xe"
)
cursor = connection.cursor()

# Function to add a new donor
def add_donor(name, age, contact_number, blood_type_id):
    try:
        # Ensure age and blood_type_id are integers
        age = int(age)  # Convert age to int
        blood_type_id = int(blood_type_id)  # Convert blood_type_id to int
        
        cursor.execute("""
            INSERT INTO Donors (donor_id, name, age, contact_number, blood_type_id)
            VALUES ((SELECT NVL(MAX(donor_id), 0) + 1 FROM Donors), :name, :age, :contact_number, :blood_type_id)
        """, [name, age, contact_number, blood_type_id])
        connection.commit()
        return "Donor added successfully."
    except oracledb.Error as error:
        return f"Error occurred: {error}"

# Function to check blood availability
def check_blood_availability(blood_type_id):
    try:
        blood_type_id = int(blood_type_id)  # Ensure blood_type_id is an integer
        cursor.execute("SELECT available_units FROM Blood_Types WHERE blood_type_id = :blood_type_id", [blood_type_id])
        result = cursor.fetchone()
        if result:
            return result[0]
        return "Blood type not found."
    except oracledb.Error as error:
        return f"Error occurred: {error}"

# Function to book a reservation
def book_reservation(donor_id, reservation_time, status):
    try:
        donor_id = int(donor_id)  # Ensure donor_id is an integer
        cursor.execute("""
            INSERT INTO Reservations (reservation_id, donor_id, reservation_date, reservation_time, status)
            VALUES ((SELECT NVL(MAX(reservation_id), 0) + 1 FROM Reservations), :donor_id, SYSDATE, :reservation_time, :status)
        """, [donor_id, reservation_time, status])
        connection.commit()
        return "Reservation booked successfully."
    except oracledb.Error as error:
        return f"Error occurred: {error}"

# Function to get all blood types and available units
def get_all_blood_types():
    try:
        cursor.execute("SELECT blood_type, available_units FROM Blood_Types")
        results = cursor.fetchall()
        return results
    except oracledb.Error as error:
        return f"Error occurred: {error}"

# Function to update donor information
def update_donor(donor_id, name, age, contact_number, blood_type_id):
    try:
        age = int(age)  # Convert age to int
        blood_type_id = int(blood_type_id)  # Convert blood_type_id to int

        cursor.execute("""
            UPDATE Donors
            SET name = :name, age = :age, contact_number = :contact_number, blood_type_id = :blood_type_id
            WHERE donor_id = :donor_id
        """, [name, age, contact_number, blood_type_id, donor_id])
        connection.commit()
        return "Donor updated successfully."
    except oracledb.Error as error:
        return f"Error occurred: {error}"

# Function to update reservation status
def update_reservation_status(reservation_id, new_status):
    try:
        cursor.execute("""
            UPDATE Reservations
            SET status = :new_status
            WHERE reservation_id = :reservation_id
        """, [new_status, reservation_id])
        connection.commit()
        return "Reservation status updated successfully."
    except oracledb.Error as error:
        return f"Error occurred: {error}"

# db_operations.py

def get_donor_details():
    """
    Retrieve detailed information about donors, including their blood type and availability.
    """
    try:
        query = """
            SELECT d.donor_id, d.name, d.age, d.contact_number, bt.blood_type, bt.available_units
            FROM Donors d
            JOIN Blood_Types bt ON d.blood_type_id = bt.blood_type_id
            ORDER BY d.donor_id
        """
        cursor.execute(query)
        donor_details = cursor.fetchall()
        return donor_details
    except oracledb.Error as error:
        return f"Error occurred: {error}"


# New function using a subquery
def get_top_donors():
    try:

        query = """
            SELECT donor_id, name, age, contact_number
            FROM donors
            WHERE donor_id IN (
                SELECT donor_id
                FROM reservations
                GROUP BY donor_id
                HAVING COUNT(donor_id) = (
                    SELECT MAX(donor_count) 
                    FROM (SELECT donor_id, COUNT(donor_id) AS donor_count
                          FROM reservations
                          GROUP BY donor_id)
                )
            )
        """
        
        cursor.execute(query)
        top_donors = cursor.fetchall()
        return top_donors

    except oracledb.DatabaseError as e:
        return f"Error: {e}"
    

# Close the database connection when done
def close_connection():
    cursor.close()
    connection.close()
