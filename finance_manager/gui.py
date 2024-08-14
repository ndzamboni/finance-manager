import tkinter as tk
from tkinter import messagebox
from datetime import datetime  # Import the datetime module

from .auth import login_user, register_user
from .transactions import add_transaction, edit_transaction, delete_transaction, view_transactions
from .models import Transaction

def show_login_window():
    login_window = tk.Tk()
    login_window.title("Login")

    tk.Label(login_window, text="Username:").grid(row=0, column=0)
    tk.Label(login_window, text="Password:").grid(row=1, column=0)

    username_entry = tk.Entry(login_window)
    password_entry = tk.Entry(login_window, show="*")

    username_entry.grid(row=0, column=1)
    password_entry.grid(row=1, column=1)

    def login_action():
        username = username_entry.get()
        password = password_entry.get()
        user_id = login_user(username, password)
        if user_id:
            login_window.destroy()
            show_main_window(user_id)

    tk.Button(login_window, text="Login", command=login_action).grid(row=2, column=1)
    tk.Button(login_window, text="Register", command=lambda: show_register_window(login_window)).grid(row=2, column=0)

    login_window.mainloop()

def show_register_window(parent_window):
    register_window = tk.Toplevel(parent_window)
    register_window.title("Register")

    tk.Label(register_window, text="Username:").grid(row=0, column=0)
    tk.Label(register_window, text="Password:").grid(row=1, column=0)

    username_entry = tk.Entry(register_window)
    password_entry = tk.Entry(register_window, show="*")

    username_entry.grid(row=0, column=1)
    password_entry.grid(row=1, column=1)

    def register_action():
        username = username_entry.get()
        password = password_entry.get()
        register_user(username, password)
        messagebox.showinfo("Registration", "Registration successful!")
        register_window.destroy()

    tk.Button(register_window, text="Register", command=register_action).grid(row=2, column=1)

def show_main_window(user_id):
    main_window = tk.Tk()
    main_window.title("Finance Manager")

    def add_transaction_action():
        date = date_entry.get()
        amount = amount_entry.get()
        category = category_entry.get()
        description = description_entry.get()
        transaction_type = transaction_type_var.get()
        if validate_date(date) and validate_amount(amount):
            transaction = Transaction(date, float(amount), category, description, transaction_type)
            add_transaction(user_id, transaction)
            messagebox.showinfo("Success", "Transaction added successfully!")
            clear_entries()
        else:
            messagebox.showerror("Error", "Invalid input.")

    def view_transactions_action():
        transactions_window = tk.Toplevel(main_window)
        transactions_window.title("View Transactions")
        rows = view_transactions(user_id)
        if rows:
            for index, transaction in enumerate(rows):
                tk.Label(transactions_window, text=f"{transaction[2]} | {transaction[3]} | {transaction[4]} | {transaction[5]} | {transaction[6]}").grid(row=index, column=0)
        else:
            tk.Label(transactions_window, text="No transactions found.").grid(row=0, column=0)

    def edit_transaction_action():
        transaction_id = transaction_id_entry.get()
        if transaction_id.isdigit():
            edit_transaction(user_id, int(transaction_id))
        else:
            messagebox.showerror("Error", "Invalid transaction ID.")

    def delete_transaction_action():
        transaction_id = transaction_id_entry.get()
        if transaction_id.isdigit():
            delete_transaction(user_id, int(transaction_id))
        else:
            messagebox.showerror("Error", "Invalid transaction ID.")

    def clear_entries():
        date_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)
        category_entry.delete(0, tk.END)
        description_entry.delete(0, tk.END)
        transaction_type_var.set("expense")

    # Transaction fields
    tk.Label(main_window, text="Date (YYYY-MM-DD):").grid(row=0, column=0)
    tk.Label(main_window, text="Amount:").grid(row=1, column=0)
    tk.Label(main_window, text="Category:").grid(row=2, column=0)
    tk.Label(main_window, text="Description:").grid(row=3, column=0)
    tk.Label(main_window, text="Type:").grid(row=4, column=0)

    date_entry = tk.Entry(main_window)
    amount_entry = tk.Entry(main_window)
    category_entry = tk.Entry(main_window)
    description_entry = tk.Entry(main_window)
    transaction_type_var = tk.StringVar(value="expense")
    tk.Radiobutton(main_window, text="Expense", variable=transaction_type_var, value="expense").grid(row=4, column=1)
    tk.Radiobutton(main_window, text="Income", variable=transaction_type_var, value="income").grid(row=4, column=2)

    date_entry.grid(row=0, column=1)
    amount_entry.grid(row=1, column=1)
    category_entry.grid(row=2, column=1)
    description_entry.grid(row=3, column=1)

    tk.Button(main_window, text="Add Transaction", command=add_transaction_action).grid(row=5, column=1)
    tk.Button(main_window, text="View Transactions", command=view_transactions_action).grid(row=6, column=1)
    tk.Label(main_window, text="Transaction ID:").grid(row=7, column=0)
    transaction_id_entry = tk.Entry(main_window)
    transaction_id_entry.grid(row=7, column=1)
    tk.Button(main_window, text="Edit Transaction", command=edit_transaction_action).grid(row=8, column=0)
    tk.Button(main_window, text="Delete Transaction", command=delete_transaction_action).grid(row=8, column=1)

    main_window.mainloop()

def validate_date(date_text):
    try:
        datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validate_amount(amount_text):
    try:
        amount = float(amount_text)
        return amount > 0
    except ValueError:
        return False
