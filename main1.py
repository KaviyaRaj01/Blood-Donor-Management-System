from tkinter import *
from tkinter import messagebox
from db_operations2 import (
    add_donor,
    check_blood_availability,
    book_reservation,
    get_all_blood_types,
    update_donor,
    update_reservation_status,
    get_donor_details,
    get_top_donors
)

# Main GUI setup
def add_donor_gui():
    def submit_donor():
        name = name_entry.get()
        age = age_entry.get()
        contact_number = contact_entry.get()
        blood_type_id = blood_type_entry.get()

        if not age.isdigit() or not blood_type_id.isdigit():
            messagebox.showerror("Input Error", "Age and Blood Type ID must be integers.")
            return

        message = add_donor(name, int(age), contact_number, int(blood_type_id))
        messagebox.showinfo("Add Donor", message)
        add_window.destroy()

    add_window = Toplevel(root)
    add_window.title("Add Donor")

    Label(add_window, text="Name:").pack()
    name_entry = Entry(add_window, font=("Helvetica", 14), width=30)
    name_entry.pack(pady=5)

    Label(add_window, text="Age:").pack()
    age_entry = Entry(add_window, font=("Helvetica", 14), width=30)
    age_entry.pack(pady=5)

    Label(add_window, text="Contact Number:").pack()
    contact_entry = Entry(add_window, font=("Helvetica", 14), width=30)
    contact_entry.pack(pady=5)

    Label(add_window, text="Blood Type ID:").pack()
    blood_type_entry = Entry(add_window, font=("Helvetica", 14), width=30)
    blood_type_entry.pack(pady=5)

    submit_button = Button(add_window, text="Submit", command=submit_donor, font=("Helvetica", 14))
    submit_button.pack(pady=10)

def check_blood_availability_gui():
    def check_blood():
        blood_type_id = blood_type_entry.get()

        if not blood_type_id.isdigit():
            messagebox.showerror("Input Error", "Blood Type ID must be an integer.")
            return

        available_units = check_blood_availability(int(blood_type_id))
        messagebox.showinfo("Blood Availability", f"Available Units: {available_units}")
        check_window.destroy()

    check_window = Toplevel(root)
    check_window.title("Check Blood Availability")

    Label(check_window, text="Blood Type ID:").pack()
    blood_type_entry = Entry(check_window, font=("Helvetica", 14), width=30)
    blood_type_entry.pack(pady=5)

    check_button = Button(check_window, text="Check", command=check_blood, font=("Helvetica", 14))
    check_button.pack(pady=10)

def book_reservation_gui():
    def submit_reservation():
        donor_id = donor_id_entry.get()
        reservation_time = time_entry.get()
        status='Scheduled'

        if not donor_id.isdigit():
            messagebox.showerror("Input Error", "Donor ID must be an integer.")
            return

        message = book_reservation(int(donor_id), reservation_time, status)
        messagebox.showinfo("Book Reservation", message)
        book_window.destroy()

    book_window = Toplevel(root)
    book_window.title("Book Reservation")

    Label(book_window, text="Donor ID:").pack()
    donor_id_entry = Entry(book_window, font=("Helvetica", 14), width=30)
    donor_id_entry.pack(pady=5)

    Label(book_window, text="Reservation Time:").pack()
    time_entry = Entry(book_window, font=("Helvetica", 14), width=30)
    time_entry.pack(pady=5)

    submit_button = Button(book_window, text="Submit", command=submit_reservation, font=("Helvetica", 14))
    submit_button.pack(pady=10)

def show_blood_types_gui():
    blood_types = get_all_blood_types()
    blood_window = Toplevel(root)
    blood_window.title("Available Blood Types and Units")

    Label(blood_window, text="Blood Type").grid(row=0, column=0, padx=10, pady=5)
    Label(blood_window, text="Available Units").grid(row=0, column=1, padx=10, pady=5)

    for i, (blood_type, units) in enumerate(blood_types, start=1):
        Label(blood_window, text=blood_type).grid(row=i, column=0, padx=10, pady=5)
        Label(blood_window, text=units).grid(row=i, column=1, padx=10, pady=5)


def update_donor_gui():
    def submit_update():
        donor_id = donor_id_entry.get()
        name = name_entry.get()
        age = age_entry.get()
        contact_number = contact_entry.get()
        blood_type_id = blood_type_entry.get()

        message = update_donor(donor_id, name, age, contact_number, blood_type_id)
        messagebox.showinfo("Update Donor", message)
        update_window.destroy()

    update_window = Toplevel(root)
    update_window.title("Update Donor")

    Label(update_window, text="Donor ID:").pack()
    donor_id_entry = Entry(update_window, font=("Helvetica", 14), width=30)
    donor_id_entry.pack(pady=5)

    Label(update_window, text="Name:").pack()
    name_entry = Entry(update_window, font=("Helvetica", 14), width=30)
    name_entry.pack(pady=5)

    Label(update_window, text="Age:").pack()
    age_entry = Entry(update_window, font=("Helvetica", 14), width=30)
    age_entry.pack(pady=5)

    Label(update_window, text="Contact Number:").pack()
    contact_entry = Entry(update_window, font=("Helvetica", 14), width=30)
    contact_entry.pack(pady=5)

    Label(update_window, text="Blood Type ID:").pack()
    blood_type_entry = Entry(update_window, font=("Helvetica", 14), width=30)
    blood_type_entry.pack(pady=5)

    submit_button = Button(update_window, text="Update", command=submit_update, font=("Helvetica", 14))
    submit_button.pack(pady=10)

def update_reservation_status_gui():
    def submit_status_update():
        reservation_id = reservation_id_entry.get()
        new_status = status_entry.get()

        message = update_reservation_status(reservation_id, new_status)
        messagebox.showinfo("Update Reservation Status", message)
        status_update_window.destroy()

    status_update_window = Toplevel(root)
    status_update_window.title("Update Reservation Status")

    Label(status_update_window, text="Reservation ID:").pack()
    reservation_id_entry = Entry(status_update_window, font=("Helvetica", 14), width=30)
    reservation_id_entry.pack(pady=5)

    Label(status_update_window, text="New Status:").pack()
    status_entry = Entry(status_update_window, font=("Helvetica", 14), width=30)
    status_entry.pack(pady=5)

    submit_button = Button(status_update_window, text="Update", command=submit_status_update, font=("Helvetica", 14))
    submit_button.pack(pady=10)

def show_donor_details_gui():
    donor_details = get_donor_details()
    details_window = Toplevel(root)
    details_window.title("Donor Details with Blood Type Information")

    for donor in donor_details:
        Label(details_window, text=f"ID: {donor[0]}, Name: {donor[1]}, Age: {donor[2]}, Contact: {donor[3]}, Blood Type: {donor[4]}, Units: {donor[5]}").pack(pady=2)

def show_top_donors_gui():
    top_donors = get_top_donors()
    top_donors_window = Toplevel(root)
    top_donors_window.title("Top Donors by Reservation Count")

    Label(top_donors_window, text="Donor ID").pack()
    Label(top_donors_window, text="Name").pack()
    Label(top_donors_window, text="Age").pack()
    Label(top_donors_window, text="Contact Number").pack()

    for donor in top_donors:
        Label(top_donors_window, text=f"ID: {donor[0]}, Name: {donor[1]}, Age: {donor[2]}, Contact: {donor[3]}").pack()

# Main Tkinter window
root = Tk()
root.title("🩸Blood Donor Reservation System")

# Load the background image
background_image = PhotoImage(file=r'E:\DBMS_final\images\background2.png')  # Use raw string
background_label = Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Fill the entire window

# Load the logo image
logo_image = PhotoImage(file=r'E:\DBMS_final\images\logo2.png')  # Use raw string
logo_label = Label(root, image=logo_image, width=700)
logo_label.pack(pady=10)

# Adjust the font size for buttons
button_font = ("Helvetica", 14)

# Create buttons using pack
Button(root, text="Add Donor", command=add_donor_gui, font=button_font).pack(pady=10)
Button(root, text="Check Blood Availability", command=check_blood_availability_gui, font=button_font).pack(pady=10)
Button(root, text="Book Reservation", command=book_reservation_gui, font=button_font).pack(pady=10)
Button(root, text="Show Blood Types", command=show_blood_types_gui, font=button_font).pack(pady=10)
Button(root, text="Update Donor", command=update_donor_gui, font=button_font).pack(pady=10)
Button(root, text="Update Reservation Status", command=update_reservation_status_gui, font=button_font).pack(pady=10)
Button(root, text="Show Donor Details", command=show_donor_details_gui, font=button_font).pack(pady=10)
Button(root, text="Show Top Donors", command=show_top_donors_gui, font=("Helvetica", 14)).pack(pady=10)

root.mainloop()
