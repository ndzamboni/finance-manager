import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime  # Import the datetime module

from .auth import login_user, register_user
from .transactions import add_transaction, edit_transaction, delete_transaction, view_transactions
from .models import Transaction
from .visualization import plot_income_expense_trend, plot_monthly_expenses
from .reports import generate_yearly_summary, generate_monthly_report


def create_menu_bar(main_window, user_id):
    menu_bar = tk.Menu(main_window)
    
    # File Menu
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Exit", command=main_window.quit)
    menu_bar.add_cascade(label="File", menu=file_menu)

    # Reports Menu
    reports_menu = tk.Menu(menu_bar, tearoff=0)
    reports_menu.add_command(label="Monthly Report", command=lambda: generate_monthly_report(user_id, '2024', '08'))
    reports_menu.add_command(label="Yearly Report", command=lambda: generate_yearly_summary(user_id, '2024'))
    reports_menu.add_command(label="Income vs Expense", command=lambda: plot_income_expense_trend(user_id))
    reports_menu.add_command(label="Monthly Expenses", command=lambda: plot_monthly_expenses(user_id, '2024'))
    menu_bar.add_cascade(label="Reports", menu=reports_menu)

    # Help Menu
    help_menu = tk.Menu(menu_bar, tearoff=0)
    help_menu.add_command(label="About", command=lambda: messagebox.showinfo("About", "Finance Manager v1.0"))
    menu_bar.add_cascade(label="Help", menu=help_menu)

    main_window.config(menu=menu_bar)


def show_login_window():
    login_window = tk.Tk()
    login_window.title("Login")

    ttk.Label(login_window, text="Username:").grid(row=0, column=0, padx=10, pady=10)
    ttk.Label(login_window, text="Password:").grid(row=1, column=0, padx=10, pady=10)

    username_entry = ttk.Entry(login_window)
    password_entry = ttk.Entry(login_window, show="*")

    username_entry.grid(row=0, column=1, padx=10, pady=10)
    password_entry.grid(row=1, column=1, padx=10, pady=10)

    def login_action():
        username = username_entry.get()
        password = password_entry.get()
        user_id = login_user(username, password)
        if user_id:
            login_window.destroy()
            show_main_window(user_id)

    ttk.Button(login_window, text="Login", command=login_action).grid(row=2, column=1, pady=10)
    ttk.Button(login_window, text="Register", command=lambda: show_register_window(login_window)).grid(row=2, column=0, pady=10)

    login_window.mainloop()

def show_register_window(parent_window):
    register_window = tk.Toplevel(parent_window)
    register_window.title("Register")

    ttk.Label(register_window, text="Username:").grid(row=0, column=0, padx=10, pady=10)
    ttk.Label(register_window, text="Password:").grid(row=1, column=0, padx=10, pady=10)

    username_entry = ttk.Entry(register_window)
    password_entry = ttk.Entry(register_window, show="*")

    username_entry.grid(row=0, column=1, padx=10, pady=10)
    password_entry.grid(row=1, column=1, padx=10, pady=10)

    def register_action():
        username = username_entry.get()
        password = password_entry.get()
        register_user(username, password)
        messagebox.showinfo("Registration", "Registration successful!")
        register_window.destroy()

    ttk.Button(register_window, text="Register", command=register_action).grid(row=2, column=1, pady=10)

def show_main_window(user_id):
    main_window = tk.Tk()
    main_window.title("Finance Manager")

    # Create a menu bar
    create_menu_bar(main_window, user_id)

    # Modern TTK styling
    style = ttk.Style()
    style.configure("TButton", font=("Arial", 10))
    style.configure("TLabel", font=("Arial", 12))

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

    def get_selected_transaction_id():
        selected_index = transaction_list.curselection()
        if selected_index:
            return transaction_ids[selected_index[0]]  # Return the ID of the selected transaction
        else:
            messagebox.showerror("Error", "No transaction selected.")
            return None

    def edit_transaction_action():
        transaction_id = get_selected_transaction_id()
        if transaction_id:
            edit_transaction(user_id, transaction_id)

    def delete_transaction_action():
        transaction_id = get_selected_transaction_id()
        if transaction_id:
            delete_transaction(user_id, transaction_id)

    def view_transactions_action():
        transactions_window = tk.Toplevel(main_window)
        transactions_window.title("View Transactions")

        # Adding a scrollbar for better viewing
        scrollbar = tk.Scrollbar(transactions_window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Creating a Listbox widget to display transactions
        global transaction_list
        transaction_list = tk.Listbox(transactions_window, yscrollcommand=scrollbar.set, width=100, selectmode=tk.SINGLE)
        scrollbar.config(command=transaction_list.yview)

        global transaction_ids
        transaction_ids = []  # To keep track of transaction IDs

        rows = view_transactions(user_id)
        if rows:
            for index, transaction in enumerate(rows):
                transaction_list.insert(tk.END, f"{transaction[0]}: Date: {transaction[2]} | Amount: {transaction[3]} | Category: {transaction[4]} | Description: {transaction[5]} | Type: {transaction[6]}")
                transaction_ids.append(transaction[0])  # Store the transaction ID
        else:
            transaction_list.insert(tk.END, "No transactions found.")

        transaction_list.pack(side=tk.LEFT, fill=tk.BOTH)

        ttk.Button(transactions_window, text="Edit Selected Transaction", command=edit_transaction_action).pack(side=tk.LEFT, padx=10, pady=10)
        ttk.Button(transactions_window, text="Delete Selected Transaction", command=delete_transaction_action).pack(side=tk.RIGHT, padx=10, pady=10)

    def clear_entries():
        date_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)
        category_entry.delete(0, tk.END)
        description_entry.delete(0, tk.END)
        transaction_type_var.set("expense")

    # Transaction fields using TTK widgets
    ttk.Label(main_window, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=10, pady=10)
    ttk.Label(main_window, text="Amount:").grid(row=1, column=0, padx=10, pady=10)
    ttk.Label(main_window, text="Category:").grid(row=2, column=0, padx=10, pady=10)
    ttk.Label(main_window, text="Description:").grid(row=3, column=0, padx=10, pady=10)
    ttk.Label(main_window, text="Type:").grid(row=4, column=0, padx=10, pady=10)

    date_entry = ttk.Entry(main_window)
    amount_entry = ttk.Entry(main_window)
    category_entry = ttk.Entry(main_window)
    description_entry = ttk.Entry(main_window)
    transaction_type_var = tk.StringVar(value="expense")
    ttk.Radiobutton(main_window, text="Expense", variable=transaction_type_var, value="expense").grid(row=4, column=1)
    ttk.Radiobutton(main_window, text="Income", variable=transaction_type_var, value="income").grid(row=4, column=2)

    date_entry.grid(row=0, column=1, padx=10, pady=10)
    amount_entry.grid(row=1, column=1, padx=10, pady=10)
    category_entry.grid(row=2, column=1, padx=10, pady=10)
    description_entry.grid(row=3, column=1, padx=10, pady=10)

    ttk.Button(main_window, text="Add Transaction", command=add_transaction_action).grid(row=5, column=1, pady=10)
    ttk.Button(main_window, text="View Transactions", command=view_transactions_action).grid(row=6, column=1, pady=10)

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
