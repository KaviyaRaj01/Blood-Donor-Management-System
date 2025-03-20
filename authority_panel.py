from tkinter import *
from tkinter import messagebox
import subprocess

# Function to handle login
def login():
    username = username_entry.get()
    password = password_entry.get()

    if username == "admin" and password == "password":
        messagebox.showinfo("Login Successful", "Welcome!")
        login_window.destroy()  # Close the login window
        subprocess.run(["python", "main1.py"])  # Adjust if main1.py is in a different location
    else:
        messagebox.showerror("Login Failed", "Invalid credentials. Please try again.")

# Set up the login window
login_window = Tk()
login_window.title("Authority Login")
login_window.geometry("350x250")
login_window.config(bg="#f2f2f2")

# Center window on the screen
window_width, window_height = 350, 250
screen_width = login_window.winfo_screenwidth()
screen_height = login_window.winfo_screenheight()
x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))
login_window.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

# Logo
logo_label = Label(login_window, text="🩸 Blood Donor System", font=("Helvetica", 16, "bold"), bg="#f2f2f2", fg="#cc0000")
logo_label.pack(pady=15)

# Username entry
username_label = Label(login_window, text="Username:", font=("Helvetica", 12), bg="#f2f2f2")
username_label.pack(pady=5)
username_entry = Entry(login_window, font=("Helvetica", 12), width=25)
username_entry.pack()

# Password entry
password_label = Label(login_window, text="Password:", font=("Helvetica", 12), bg="#f2f2f2")
password_label.pack(pady=5)
password_entry = Entry(login_window, font=("Helvetica", 12), show="*", width=25)
password_entry.pack()

# Login button
login_button = Button(login_window, text="Login", command=login, font=("Helvetica", 12, "bold"), bg="#cc0000", fg="white", width=10)
login_button.pack(pady=20)

login_window.mainloop()
