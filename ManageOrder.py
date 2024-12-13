import tkinter as tk
from tkinter import messagebox, ttk, END
import locale
import mysql.connector
from Batch1 import ManageProduct  # Ensure Batch1 is imported correctly
from datetime import datetime

locale.setlocale(locale.LC_ALL, '')  # Set locale for currency formatting


class ManageOrder(tk.Tk):
    def __init__(self):
        super().__init__()
        self.overrideredirect(1)  # Make the window undecorated
        self.title("Manage Order")
        self.geometry("1410x750")
        self.configure(bg='#FF99FF')

        # Initialize variables
        self.finalTotalPrice = 0.0

        # Create widgets
        self.create_widgets()
        self.center_table_text()
        self.center_table_header()

        # Add Menu Bar
        self.create_menu_bar()

        # Load products into table
        self.load_products()

    def create_menu_bar(self):
        menu_bar = tk.Menu(self)

        inventory_menu = tk.Menu(menu_bar, tearoff=0)
        inventory_menu.add_command(label="Products", command=lambda: self.select_batch(ManageProduct))

        menu_bar.add_cascade(label="Inventory", menu=inventory_menu)
        self.config(menu=menu_bar)

    def select_batch(self, manage_product_class):
        """Handles the batch selection from the menu."""
        try:
            # Initialize and open the `ManageProduct` window without arguments.
            batch_window = manage_product_class()  # If no parameters are expected
            batch_window.mainloop()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open Batch 1: {str(e)}")

    def create_widgets(self):
        lbl_product_list = tk.Label(self, text="Product List", font=("Powerhouse Sans", 30), bg='#FF99FF')
        lbl_product_list.place(x=290, y=10)

        lbl_cart = tk.Label(self, text="Cart", font=("Powerhouse Sans", 30), bg='#FF99FF')
        lbl_cart.place(x=1020, y=10)

        lbl_selected_product = tk.Label(self, text="Selected Product:", font=("Powerhouse Sans", 20), bg='#FF99FF')
        lbl_selected_product.place(x=300, y=330)

        lbl_product_name = tk.Label(self, text="Product Name", font=("Powerhouse Sans", 18), bg='#FF99FF')
        lbl_product_name.place(x=320, y=370)

        lbl_product_price = tk.Label(self, text="Product Price", font=("Powerhouse Sans", 18), bg='#FF99FF')
        lbl_product_price.place(x=320, y=440)

        lbl_product_expired = tk.Label(self, text="Expiration Date", font=("Powerhouse Sans", 18), bg='#FF99FF')
        lbl_product_expired.place(x=310, y=510)

        lbl_quantity = tk.Label(self, text="Quantity", font=("Powerhouse Sans", 18), bg='#FF99FF')
        lbl_quantity.place(x=320, y=580)

        self.table_product = ttk.Treeview(
            self,
            columns=("Name", "Quantity", "Price", "Expiration Date"),
            show="headings"
        )
        self.table_product.heading("Name", text="Name")
        self.table_product.heading("Quantity", text="Quantity")
        self.table_product.heading("Price", text="Price")
        self.table_product.heading("Expiration Date", text="Expiration Date")
        self.table_product.column("Name", width=150)
        self.table_product.column("Quantity", width=100)
        self.table_product.column("Price", width=100)
        self.table_product.column("Expiration Date", width=150)
        self.table_product.place(x=20, y=60, width=660, height=260)
        self.table_product.bind("<ButtonRelease-1>", self.on_product_select)

        self.table_cart = ttk.Treeview(
            self,
            columns=("Name", "Quantity", "Price", "Expiration Date", "Total"),
            show="headings"
        )
        self.table_cart.heading("Name", text="Name")
        self.table_cart.heading("Quantity", text="Quantity")
        self.table_cart.heading("Price", text="Price")
        self.table_cart.heading("Expiration Date", text="Expiration Date")
        self.table_cart.heading("Total", text="Total")
        self.table_cart.column("Name", width=150)
        self.table_cart.column("Quantity", width=100)
        self.table_cart.column("Price", width=100)
        self.table_cart.column("Expiration Date", width=150)
        self.table_cart.column("Total", width=100)
        self.table_cart.place(x=690, y=60, width=650, height=260)

        scrollbar_cart = ttk.Scrollbar(self, orient="vertical", command=self.table_cart.yview)
        scrollbar_cart.place(x=1360, y=60, height=260)
        self.table_cart.configure(yscroll=scrollbar_cart.set)

        self.txt_product_name = tk.Entry(self, font=("Segoe UI", 18), justify='center')
        self.txt_product_name.place(x=180, y=400, width=400, height=30)

        self.txt_product_price = tk.Entry(self, font=("Segoe UI", 18), justify='center')
        self.txt_product_price.place(x=180, y=470, width=400, height=30)

        self.txt_product_expired = tk.Entry(self, font=("Segoe UI", 18), justify='center')
        self.txt_product_expired.place(x=180, y=540, width=400, height=30)

        self.txt_order_quantity = tk.Entry(self, font=("Segoe UI", 18), justify='center')
        self.txt_order_quantity.place(x=180, y=610, width=400, height=30)

        btn_add_to_cart = tk.Button(self, text="Add tCart", command=self.add_to_cart, bg='#001452', fg='white')
        btn_add_to_cart.place(x=270, y=670, width=210, height=40)

        self.txt_pay = tk.Entry(self, font=("Segoe UI", 18), justify='center')
        self.txt_pay.place(x=1010, y=430, width=130, height=40)

        self.txt_total = tk.Entry(self, font=("Segoe UI", 18), justify='center')
        self.txt_total.place(x=1010, y=360, width=130, height=40)

        self.txt_bal = tk.Entry(self, font=("Segoe UI", 18), justify='center')
        self.txt_bal.place(x=1020, y=500, width=110, height=40)

        lbl_total = tk.Label(self, text="TOTAL:", font=("Powerhouse Sans", 24), bg='#FF99FF', fg='black')
        lbl_total.place(x=900, y=360)

        lbl_cash = tk.Label(self, text="CASH:", font=("Powerhouse Sans", 24), bg='#FF99FF', fg='black')
        lbl_cash.place(x=920, y=430)

        lbl_change = tk.Label(self, text="CHANGE:", font=("Segoe UI", 24), bg='#FF99FF', fg='black')
        lbl_change.place(x=870, y=490)

        self.add_functional_buttons()

    def add_functional_buttons(self):
        btn_save_order = tk.Button(self, text="ENTER", command=self.save_order, bg='#001452', fg='white',
                                   font=("Segoe UI", 14))
        btn_save_order.place(x=980, y=580, width=200, height=50)

        btn_refresh = tk.Button(self, text="REFRESH", command=self.refresh, bg='#001452', fg='white',
                                font=("Segoe UI", 14))
        btn_refresh.place(x=980, y=650, width=200, height=50)

        btn_close = tk.Button(self, text="Close", command=self.destroy, bg='#CC0000', fg='white')
        btn_close.place(x=1260, y=710, width=100, height=30)

    def on_product_select(self, event):
        """Handles product selection by placing data in fields."""
        # Get the currently selected row index
        selected_item = self.table_product.selection()
        if selected_item:
            # Retrieve data from the selected row
            item = self.table_product.item(selected_item)
            name, _, price, expiration_date = item['values']

            # Set the text fields with the selected row's data, excluding the quantity.
            self.txt_product_name.config(state='normal')
            self.txt_product_name.delete(0, END)
            self.txt_product_name.insert(END, name)
            self.txt_product_name.config()

            self.txt_product_price.config(state='normal')
            self.txt_product_price.delete(0, END)
            self.txt_product_price.insert(END, price)
            self.txt_product_price.config()

            self.txt_product_expired.config(state='normal')
            self.txt_product_expired.delete(0, END)
            self.txt_product_expired.insert(END, expiration_date)
            self.txt_product_expired.config()

    def load_products(self):
        """Loads products from the database and populates the table."""
        try:
            con = mysql.connector.connect(
                host='localhost',
                user='root',
                password='041423',
                database='appuser'
            )
            cursor = con.cursor(buffered=True)  # Use a buffered cursor

            cursor.execute("SELECT name, quantity, price, expirationDate FROM product")

            # Clear existing product table data
            for row in self.table_product.get_children():
                self.table_product.delete(row)

            # Fetch and populate rows
            for row in cursor.fetchall():
                self.table_product.insert('', 'end', values=row)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
        finally:
            if con.is_connected():
                con.close()

    def create_entry_with_label(self, text, x, y):
        lbl = tk.Label(self, text=text, font=("Powerhouse Sans", 18), bg='#FF99FF')
        lbl.place(x=x - 140, y=y)
        entry = tk.Entry(self, font=("Segoe UI", 18), justify='center', state='disabled')
        entry.place(x=180, y=y + 30, width=400, height=30)
        return entry

    def center_table_text(self):
        for col in self.table_product['columns']:
            self.table_product.column(col, anchor='center')
        for col in self.table_cart['columns']:
            self.table_cart.column(col, anchor='center')

    def center_table_header(self):
        for col in self.table_product['columns']:
            self.table_product.heading(col, anchor='center')
        for col in self.table_cart['columns']:
            self.table_cart.heading(col, anchor='center')


    def add_to_cart(self):
        no_of_units = self.txt_order_quantity.get()
        if no_of_units:
            product_name = self.txt_product_name.get()
            product_price = self.txt_product_price.get()
            product_expired = self.txt_product_expired.get()

            # Check if the product is expired
            try:
                expiration_date = datetime.strptime(product_expired, '%Y-%m-%d')  # Convert to datetime
                current_date = datetime.now()  # Get the current date

                if expiration_date < current_date:  # Compare expiration date with the current date
                    messagebox.showwarning("Product Expired",
                                           f"The product '{product_name}' has expired and cannot be added.")
                    return
            except ValueError:
                messagebox.showerror("Invalid Date", "The expiration date format is incorrect. Please use YYYY-MM-DD.")
                return

            try:
                total_price = int(no_of_units) * float(product_price)
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid numbers for quantity and price.")
                return

            # Add product to the cart if not expired
            self.table_cart.insert('', 'end',
                                   values=(product_name, no_of_units, product_price, product_expired, total_price))
            self.finalTotalPrice += total_price
            self.txt_total.config(state='normal')
            self.txt_total.delete(0, END)
            self.txt_total.insert(0, locale.currency(self.finalTotalPrice, grouping=True))
            self.txt_total.config()
        else:
            messagebox.showwarning("Input Missing", "Please enter the quantity.")

    def on_cart_select(self, event):
        selected_item = self.table_cart.selection()
        if selected_item:
            item = self.table_cart.item(selected_item)
            response = messagebox.askyesno("Remove Product",
                                           f"Do you want to remove {item['values'][0]} from the cart?")
            if response:
                self.finalTotalPrice -= float(item['values'][4])
                self.txt_total.config(state='normal')
                self.txt_total.delete(0, END)
                self.txt_total.insert(0, locale.currency(self.finalTotalPrice, grouping=True))
                self.txt_total.config()
                self.table_cart.delete(selected_item)

    def add_functional_buttons(self):
        btn_save_order = tk.Button(self, text="ENTER", command=self.save_order, bg='#001452', fg='white',
                                   font=("Segoe UI", 14))
        btn_save_order.place(x=980, y=580, width=200, height=50)

        # Defining the Refresh button
        btn_refresh = tk.Button(self, text="REFRESH", command=self.refresh, bg='#001452', fg='white',
                                font=("Segoe UI", 14))
        btn_refresh.place(x=980, y=650, width=200, height=50)

        btn_close = tk.Button(self, text="Close", command=self.destroy, bg='#CC0000', fg='white')
        btn_close.place(x=1260, y=710, width=100, height=30)

    def refresh(self):
        """Resets the application to its initial state by clearing cart, resetting totals, and reloading products."""
        try:
            # Clear all items from the cart table
            self.table_cart.delete(*self.table_cart.get_children())

            # Reset total and balance fields
            self.finalTotalPrice = 0.0
            self.txt_total.config(state='normal')
            self.txt_total.delete(0, END)
            self.txt_total.insert(0, locale.currency(self.finalTotalPrice, grouping=True))
            self.txt_total.config()

            self.txt_bal.config(state='normal')
            self.txt_bal.delete(0, END)
            self.txt_bal.config()

            # Clear payment input field
            self.txt_pay.delete(0, END)

            # Reload products from the database
            self.load_products()

            # Reset product selection fields
            self.txt_product_name.config(state='normal')
            self.txt_product_name.delete(0, END)
            self.txt_product_name.config(state='disabled')

            self.txt_product_price.config(state='normal')
            self.txt_product_price.delete(0, END)
            self.txt_product_price.config(state='disabled')

            self.txt_product_expired.config(state='normal')
            self.txt_product_expired.delete(0, END)
            self.txt_product_expired.config(state='disabled')

            self.txt_order_quantity.delete(0, END)

            messagebox.showinfo("Info", "The window has been refreshed.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh the window: {str(e)}")

    def save_order(self):
        """Processes the order and updates product quantities in the database."""
        try:
            # Validate payment input
            pay_amount = float(self.txt_pay.get())
            if pay_amount < self.finalTotalPrice:
                messagebox.showwarning("Insufficient Payment",
                                       f"You need {locale.currency(self.finalTotalPrice - pay_amount, grouping=True)} more.")
                self.txt_bal.config(state='normal')
                self.txt_bal.delete(0, END)
                self.txt_bal.config()
                return
            else:
                balance = pay_amount - self.finalTotalPrice
                self.txt_bal.config(state='normal')
                self.txt_bal.delete(0, END)
                self.txt_bal.insert(0, locale.currency(balance, grouping=True))
                self.txt_bal.config()

            # Establish database connection
            con = mysql.connector.connect(
                host='localhost',
                user='root',
                password='041423',  # Use your actual MySQL password
                database='appuser'
            )
            cursor = con.cursor(buffered=True)

            # Iterate through cart items and update quantities
            for item in self.table_cart.get_children():
                product_details = self.table_cart.item(item, 'values')
                product_name = product_details[0]
                ordered_quantity = int(product_details[1])

                # Query the current quantity from the database
                cursor.execute("SELECT quantity FROM product WHERE name=%s", (product_name,))
                result = cursor.fetchone()

                if not result:
                    messagebox.showerror("Error",
                                         f"No product named '{product_name}' found in the database. Skipping...")
                    continue

                current_quantity = result[0]
                new_quantity = current_quantity - ordered_quantity

                if new_quantity < 0:
                    messagebox.showwarning("Stock Warning",
                                           f"Insufficient stock for '{product_name}'. Skipping this product...")
                    continue

                # Update the quantity in the database
                cursor.execute("UPDATE product SET quantity = %s WHERE name = %s", (new_quantity, product_name))

            # Commit all changes after successfully updating the cart items
            con.commit()
            messagebox.showinfo("Success", "Order has been processed and stock updated successfully!")

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Database error occurred: {err}")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for payment.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
        finally:
            # Close the database connection
            if con.is_connected():
                con.close()

        # Refresh the UI and reset all component



        # Refresh the product list to show the updated quantities


        # Clear the cart and reset total and balance


def main():
    app = ManageOrder()
    app.mainloop()


if __name__ == "__main__":
    main()
