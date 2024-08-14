import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import DateEntry

from .auth import login_user, register_user
from .transactions import add_transaction, edit_transaction, delete_transaction, view_transactions, get_transaction_by_id
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

    create_menu_bar(main_window, user_id)

    style = ttk.Style()
    style.configure("TButton", font=("Arial", 10))
    style.configure("TLabel", font=("Arial", 12))

    global transaction_listbox

    def add_transaction_action():
        date = date_entry.get()
        amount = amount_entry.get()
        category = category_entry.get()
        description = description_entry.get()
        transaction_type = "income" if income_switch.get() else "expense"
        if validate_date(date) and validate_amount(amount):
            transaction = Transaction(date, float(amount), category, description, transaction_type)
            add_transaction(user_id, transaction)
            messagebox.showinfo("Success", "Transaction added successfully!")
            clear_entries()
            refresh_transaction_listbox()
        else:
            messagebox.showerror("Error", "Invalid input.")

    def view_transactions_action():
        transactions_window = tk.Toplevel(main_window)
        transactions_window.title("View Financials")

        summary_text = tk.Text(transactions_window, wrap=tk.WORD, width=100, height=20)
        summary_text.pack(padx=10, pady=10)

        rows = view_transactions(user_id)
        if rows:
            financials = {}
            for transaction in rows:
                year_month = transaction[2][:7]
                if year_month not in financials:
                    financials[year_month] = {"income": 0, "expense": 0}
                if transaction[6] == "income":
                    financials[year_month]["income"] += transaction[3]
                else:
                    financials[year_month]["expense"] += transaction[3]

            for year_month, values in financials.items():
                net_amount = values["income"] - values["expense"]
                summary_text.insert(tk.END, f"{year_month}: Income: ${values['income']:.2f}, Expense: ${values['expense']:.2f}, Net: ${net_amount:.2f}\n")
        else:
            summary_text.insert(tk.END, "No transactions found.")

    def edit_transaction_action():
        selected_transaction = transaction_listbox.curselection()
        if selected_transaction:
            transaction_id = transaction_listbox.get(selected_transaction[0]).split('|')[0].strip()
            transaction = get_transaction_by_id(user_id, transaction_id)
            if transaction:
                date_entry.delete(0, tk.END)
                date_entry.insert(0, transaction[2])
                amount_entry.delete(0, tk.END)
                amount_entry.insert(0, transaction[3])
                category_entry.delete(0, tk.END)
                category_entry.insert(0, transaction[4])
                description_entry.delete(0, tk.END)
                description_entry.insert(0, transaction[5])
                income_switch.set(transaction[6] == "income")
                toggle_income_expense(income_button, income_switch)

                def save_changes():
                    updated_transaction = Transaction(
                        date_entry.get(), 
                        float(amount_entry.get()), 
                        category_entry.get(), 
                        description_entry.get(), 
                        "income" if income_switch.get() else "expense"
                    )
                    edit_transaction(user_id, transaction_id, updated_transaction.date, updated_transaction.amount, updated_transaction.category, updated_transaction.description, updated_transaction.transaction_type)
                    messagebox.showinfo("Success", "Transaction updated successfully!")
                    refresh_transaction_listbox()
                    clear_entries()

                save_button = ttk.Button(main_window, text="Save Changes", command=save_changes)
                save_button.grid(row=9, column=1, pady=10)
        else:
            messagebox.showerror("Error", "Please select a transaction to edit.")

    def delete_transaction_action():
        selected_transaction = transaction_listbox.curselection()
        if selected_transaction:
            transaction_id = transaction_listbox.get(selected_transaction[0]).split('|')[0].strip()
            delete_transaction(user_id, transaction_id)
            refresh_transaction_listbox()
        else:
            messagebox.showerror("Error", "Please select a transaction to delete.")

    def refresh_transaction_listbox():
        transaction_listbox.delete(0, tk.END)
        rows = view_transactions(user_id)
        for transaction in rows:
            transaction_listbox.insert(tk.END, f"{transaction[0]} | Date: {transaction[2]} | Amount: {transaction[3]} | Category: {transaction[4]} | Description: {transaction[5]} | Type: {transaction[6]}")

    def clear_entries():
        date_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)
        category_entry.delete(0, tk.END)
        description_entry.delete(0, tk.END)
        income_switch.set(False)
        toggle_income_expense(income_button, income_switch)

    def format_date(event):
        date_text = date_entry.get().replace("-", "")
        if len(date_text) >= 6:
            formatted_date = f"{date_text[:2]}-{date_text[2:4]}-{date_text[4:]}"
            date_entry.delete(0, tk.END)
            date_entry.insert(0, formatted_date)

    ttk.Label(main_window, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=10, pady=10)
    ttk.Label(main_window, text="Amount:").grid(row=1, column=0, padx=10, pady=10)
    ttk.Label(main_window, text="Category:").grid(row=2, column=0, padx=10, pady=10)
    ttk.Label(main_window, text="Description:").grid(row=3, column=0, padx=10, pady=10)
    ttk.Label(main_window, text="Type:").grid(row=4, column=0, padx=10, pady=10)

    date_entry = DateEntry(main_window, date_pattern='y-mm-dd')
    date_entry.bind("<KeyRelease>", format_date)

    amount_entry = ttk.Entry(main_window)
    category_entry = ttk.Entry(main_window)
    description_entry = ttk.Entry(main_window)

    income_switch = tk.BooleanVar(value=False)
    income_button = ttk.Button(main_window, text="Income", command=lambda: toggle_income_expense(income_button, income_switch))

    date_entry.grid(row=0, column=1, padx=10, pady=10)
    amount_entry.grid(row=1, column=1, padx=10, pady=10)
    category_entry.grid(row=2, column=1, padx=10, pady=10)
    description_entry.grid(row=3, column=1, padx=10, pady=10)
    income_button.grid(row=4, column=1, padx=10, pady=10)

    ttk.Button(main_window, text="Add Transaction", command=add_transaction_action).grid(row=5, column=1, pady=10)
    ttk.Button(main_window, text="View Financials", command=view_transactions_action).grid(row=6, column=1, pady=10)

    transaction_listbox = tk.Listbox(main_window, height=10, width=80)
    transaction_listbox.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

    ttk.Button(main_window, text="Edit Transaction", command=edit_transaction_action).grid(row=8, column=0, pady=10)
    ttk.Button(main_window, text="Delete Transaction", command=delete_transaction_action).grid(row=8, column=1, pady=10)

    refresh_transaction_listbox()

    main_window.mainloop()

def toggle_income_expense(button, switch):
    if switch.get():
        button.config(text="Expense")
        switch.set(False)
    else:
        button.config(text="Income")
        switch.set(True)

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
