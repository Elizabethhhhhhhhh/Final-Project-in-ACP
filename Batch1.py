import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector


class ManageProduct(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Manage Product")
        self.overrideredirect(1)  # Make the window undecorated

        # Set up dimensions for your window
        window_width, window_height = 850, 600
        self.geometry(f"{window_width}x{window_height}")

        # Get screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate x and y position to center the window
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # Set geometry with proper position
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.currentQuantity = 0
        self.init_components()
        self.center_table_text()
        self.center_table_header()


    def init_components(self):
        self.panel = tk.Frame(self, bg='black')
        self.panel.place(relwidth=1, relheight=1)

        # Labels with text
        self.lbl_title = tk.Label(self.panel, text="BATCH 1", font=("Powerhouse Sans", 36), fg='white', bg='black')
        self.lbl_title.place(x=320, y=0)

        self.lblName = tk.Label(self.panel, text="Name", font=("Powerhouse Sans", 18), fg='white', bg='black')
        self.lblName.place(x=290, y=270)

        self.lblQuantity = tk.Label(self.panel, text="Quantity", font=("Powerhouse Sans", 18), fg='white', bg='black')
        self.lblQuantity.place(x=290, y=340)

        self.lblPrice = tk.Label(self.panel, text="Price", font=("Powerhouse Sans", 18), fg='white', bg='black')
        self.lblPrice.place(x=290, y=410)

        self.lblExpirationDate = tk.Label(self.panel, text="Expiration Date", font=("Powerhouse Sans", 18), fg='white',
                                          bg='black')
        self.lblExpirationDate.place(x=290, y=480)

        self.txtName = tk.Entry(self.panel, font=("Segoe UI", 14), justify='center')
        self.txtName.place(x=290, y=300, width=320)

        self.txtQuantity = tk.Entry(self.panel, font=("Segoe UI", 14), justify='center')
        self.txtQuantity.place(x=290, y=370, width=320)

        self.txtPrice = tk.Entry(self.panel, font=("Segoe UI", 14), justify='center')
        self.txtPrice.place(x=290, y=440, width=320)

        self.txtExpirationDate = tk.Entry(self.panel, font=("Segoe UI", 14), justify='center')
        self.txtExpirationDate.place(x=290, y=510, width=320)

        self.btnSave = tk.Button(self.panel, text="Save", bg='#001452', fg='white', font=("Segoe UI", 14),
                                 command=self.save_product)
        self.btnSave.place(x=290, y=550)

        self.btnUpdate = tk.Button(self.panel, text="Update", bg='#001452', fg='white', font=("Segoe UI", 14),
                                   command=self.update_product)
        self.btnUpdate.place(x=370, y=550)
        self.btnUpdate.config(state='disabled')

        self.btnDelete = tk.Button(self.panel, text="Delete", bg='#001452', fg='white', font=("Segoe UI", 14),
                                   command=self.delete_product)
        self.btnDelete.place(x=460, y=550)

        self.btnClose = tk.Button(self.panel, text="Close", bg='#CC0000', fg='white', font=("Segoe UI", 14),
                                  command=self.close_window)
        self.btnClose.place(x=540, y=550)

        # Create table for products
        self.tableProduct = ttk.Treeview(self.panel, columns=("Name", "Quantity", "Price", "Expiration Date"),
                                         show='headings', selectmode='browse')
        self.tableProduct.heading("Name", text="Name")
        self.tableProduct.heading("Quantity", text="Quantity")
        self.tableProduct.heading("Price", text="Price")
        self.tableProduct.heading("Expiration Date", text="Expiration Date")

        self.tableProduct.place(x=10, y=50, width=830, height=220)
        self.tableProduct.bind('<<TreeviewSelect>>', self.on_product_selected)

        self.populate_table()

    def center_table_text(self):
        for col in self.tableProduct['columns']:
            self.tableProduct.column(col, anchor='center')

    def center_table_header(self):
        for col in self.tableProduct['columns']:
            self.tableProduct.heading(col, anchor='center')

    def populate_table(self):
        try:
            con = mysql.connector.connect(
                host='localhost',
                user='root',
                password='041423',
                database='appuser'
            )
            cursor = con.cursor()
            cursor.execute("SELECT name, quantity, price, expirationDate FROM product")

            # Clear the table before adding data
            self.tableProduct.delete(*self.tableProduct.get_children())

            for row in cursor.fetchall():
                self.tableProduct.insert('', 'end', values=row)

            con.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def save_product(self):
        name = self.txtName.get()
        quantity = self.txtQuantity.get()
        price = self.txtPrice.get()
        expiration_date = self.txtExpirationDate.get()

        try:
            con = mysql.connector.connect(
                host='localhost',
                user='root',
                password='041423',
                database='appuser'
            )
            cursor = con.cursor()
            cursor.execute(
                """
                INSERT INTO product (name, quantity, price, expirationDate)
                VALUES (%s, %s, %s, %s)
                """,
                (name, quantity, price, expiration_date)
            )
            con.commit()
            con.close()

            self.populate_table()
            messagebox.showinfo("Success", "Product added successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_product(self):
        selected_item = self.tableProduct.selection()[0]
        values = self.tableProduct.item(selected_item, 'values')

        # Assuming 'name' is a unique key or identifier
        name = self.txtName.get()
        quantity = self.txtQuantity.get()
        price = self.txtPrice.get()
        expiration_date = self.txtExpirationDate.get()
        old_name = values[0]

        try:
            con = mysql.connector.connect(
                host='localhost',
                user='root',
                password='041423',
                database='appuser'
            )
            cursor = con.cursor()
            cursor.execute(
                """
                UPDATE product SET name=%s, quantity=%s, price=%s, expirationDate=%s
                WHERE name=%s
                """,
                (name, quantity, price, expiration_date, old_name)
            )
            con.commit()
            con.close()

            self.populate_table()
            messagebox.showinfo("Success", "Product updated successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_product(self):
        selected_item = self.tableProduct.selection()[0]
        values = self.tableProduct.item(selected_item, 'values')

        # Assuming 'name' is a unique key or identifier
        name = values[0]

        try:
            con = mysql.connector.connect(
                host='localhost',
                user='root',
                password='041423',
                database='appuser'
            )
            cursor = con.cursor()
            cursor.execute(
                "DELETE FROM product WHERE name = %s",
                (name,)
            )
            con.commit()
            con.close()

            self.populate_table()
            messagebox.showinfo("Success", "Product deleted successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def close_window(self):
        self.destroy()

    def on_product_selected(self, event):
        # Handler for product row selection
        selected_item = self.tableProduct.selection()[0]
        values = self.tableProduct.item(selected_item, 'values')

        self.txtName.delete(0, tk.END)
        self.txtQuantity.delete(0, tk.END)
        self.txtPrice.delete(0, tk.END)
        self.txtExpirationDate.delete(0, tk.END)

        self.txtName.insert(tk.END, values[0])
        self.txtQuantity.insert(tk.END, values[1])
        self.txtPrice.insert(tk.END, values[2])
        self.txtExpirationDate.insert(tk.END, values[3])

        self.btnSave.config(state='disabled')
        self.btnUpdate.config(state='normal')


if __name__ == "__main__":
    app = ManageProduct()
    app.mainloop()
