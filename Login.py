import tkinter as tk
from tkinter import messagebox
import mysql.connector
from ManageOrder import ManageOrder


# Assume ManageOrder is defined as below or imported
# Implementation of ManageOrder widgets and functionalities

class Login(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Login")
        self.geometry("500x400")  # Set the window size
        self.overrideredirect(1)

        # Get screen width and height
        screen_width = self.winfo_screenwidth()  # Width of the screen
        screen_height = self.winfo_screenheight()  # Height of the screen

        # Calculate position x, y to center the window
        x = (screen_width - 500) // 2  # Horizontal center
        y = (screen_height - 400) // 2  # Vertical center

        self.geometry(f"500x400+{x}+{y}")  # Set the geometry including the position
        self.configure(bg='#000B26')

        # Email Label and Entry
        lbl_email = tk.Label(self, text="Email", font=("Segoe UI", 18), bg='#000B26', fg='white')
        lbl_email.place(x=110, y=90)
        self.txt_email = tk.Entry(self, font=("Segoe UI", 12))
        self.txt_email.place(x=110, y=130, width=310)

        # Password Label and Entry
        lbl_password = tk.Label(self, text="Password", font=("Segoe UI", 18), bg='#000B26', fg='white')
        lbl_password.place(x=110, y=170)
        self.txt_password = tk.Entry(self, show='*', font=("Segoe UI", 12))
        self.txt_password.place(x=110, y=210, width=310)

        # Login Button
        btn_login = tk.Button(self, text="Login", bg='blue', fg='white', command=self.login)
        btn_login.place(x=110, y=260, width=310)

        # Close Button
        btn_close = tk.Button(self, text="Close", bg='red', fg='white', command=self.close)
        btn_close.place(x=110, y=310, width=310)

        # Welcome Label
        lbl_welcome = tk.Label(self, text="Welcome", font=("Segoe UI", 24), bg='#000B26', fg='white')
        lbl_welcome.place(x=218, y=32)


    def login(self):
        email = self.txt_email.get().strip()
        password = self.txt_password.get().strip()

        try:
            con = mysql.connector.connect(
                host='localhost',
                database='appuser',
                user='root',
                password='041423'
            )

            cursor = con.cursor()
            query = ("SELECT * FROM appuser WHERE email = %s AND password = %s AND status = 'Active'")
            cursor.execute(query, (email, password))
            row = cursor.fetchone()

            if row:
                messagebox.showinfo("Login", "Login successful!")
                self.open_manage_order()
            else:
                messagebox.showwarning("Login Failed", "Incorrect Email or Password")

            cursor.close()
            con.close()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def open_manage_order(self):
        self.withdraw()  # Hide the login window
        manage_order = ManageOrder()
        manage_order.mainloop()
        self.destroy()  # Destroy login window when ManageOrder is closed

    def close(self):
        if messagebox.askyesno("Close", "Do you want to close the application?"):
            self.destroy()


if __name__ == "__main__":
    app = Login()
    app.mainloop()
