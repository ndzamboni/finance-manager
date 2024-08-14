import sqlite3
from models import Transaction
from datetime import datetime
import matplotlib.pyplot as plt
import bcrypt
import tkinter as tk
from tkinter import messagebox

# Database setup
conn = sqlite3.connect('data/finance_manager.db')
c = conn.cursor()

def create_tables():
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE,
                  password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS transactions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  date TEXT,
                  amount REAL,
                  category TEXT,
                  description TEXT,
                  transaction_type TEXT,
                  FOREIGN KEY(user_id) REFERENCES users(id))''')
    conn.commit()

# User Authentication Functions
def register_user(username, password):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
        conn.commit()
        print("User registered successfully.")
    except sqlite3.IntegrityError:
        print("Username already exists. Please choose a different username.")

def login_user(username, password):
    c.execute("SELECT id, password FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    if result and bcrypt.checkpw(password.encode('utf-8'), result[1]):
        print("Login successful.")
        return result[0]
    else:
        print("Invalid username or password.")
        return None

# Data handling functions
def add_transaction(user_id, transaction):
    try:
        c.execute("INSERT INTO transactions (user_id, date, amount, category, description, transaction_type) VALUES (?, ?, ?, ?, ?, ?)",
                  (user_id, transaction.date, transaction.amount, transaction.category, transaction.description, transaction.transaction_type))
        conn.commit()
    except Exception as e:
        print(f"An error occurred while adding the transaction: {e}")

def view_transactions(user_id):
    try:
        c.execute("SELECT * FROM transactions WHERE user_id = ?", (user_id,))
        rows = c.fetchall()
        if rows:
            print("Date       | Amount | Category     | Description        | Type")
            print("--------------------------------------------------------------")
            for row in rows:
                print(f"{row[2]} | {row[3]} | {row[4]} | {row[5]} | {row[6]}")
        else:
            print("No transactions found.")
    except Exception as e:
        print(f"An error occurred while viewing the transactions: {e}")

def edit_transaction(user_id, transaction_id):
    c.execute("SELECT * FROM transactions WHERE id = ? AND user_id = ?", (transaction_id, user_id))
    transaction = c.fetchone()
    if not transaction:
        print("Transaction not found.")
        return

    new_date = input(f"Enter new date (YYYY-MM-DD) [current: {transaction[2]}]: ") or transaction[2]
    new_amount = input(f"Enter new amount [current: {transaction[3]}]: ") or transaction[3]
    new_category = input(f"Enter new category [current: {transaction[4]}]: ") or transaction[4]
    new_description = input(f"Enter new description [current: {transaction[5]}]: ") or transaction[5]
    new_transaction_type = input(f"Enter new type ('income' or 'expense') [current: {transaction[6]}]: ") or transaction[6]

    try:
        c.execute("UPDATE transactions SET date = ?, amount = ?, category = ?, description = ?, transaction_type = ? WHERE id = ? AND user_id = ?",
                  (new_date, new_amount, new_category, new_description, new_transaction_type, transaction_id, user_id))
        conn.commit()
        print("Transaction updated successfully.")
    except Exception as e:
        print(f"An error occurred while updating the transaction: {e}")

def delete_transaction(user_id, transaction_id):
    try:
        c.execute("DELETE FROM transactions WHERE id = ? AND user_id = ?", (transaction_id, user_id))
        conn.commit()
        if c.rowcount > 0:
            print("Transaction deleted successfully.")
        else:
            print("Transaction not found.")
    except Exception as e:
        print(f"An error occurred while deleting the transaction: {e}")

# CLI functions
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

# GUI functions
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
        c.execute("SELECT * FROM transactions WHERE user_id = ?", (user_id,))
        transactions = c.fetchall()
        if transactions:
            for index, transaction in enumerate(transactions):
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

# Advanced Reporting Functions
def generate_monthly_report(user_id, year, month):
    try:
        c.execute("SELECT SUM(amount) FROM transactions WHERE user_id = ? AND transaction_type = 'income' AND strftime('%Y', date) = ? AND strftime('%m', date) = ?", (user_id, year, month))
        income = c.fetchone()[0] or 0
        c.execute("SELECT SUM(amount) FROM transactions WHERE user_id = ? AND transaction_type = 'expense' AND strftime('%Y', date) = ? AND strftime('%m', date) = ?", (user_id, year, month))
        expenses = c.fetchone()[0] or 0
    except Exception as e:
        print(f"An error occurred while generating the monthly report: {e}")
        return

    print(f"\n--- {month}-{year} Report ---")
    print(f"Total Income: ${income:.2f}")
    print(f"Total Expenses: ${expenses:.2f}")
    print(f"Net Savings: ${income - expenses:.2f}")

def generate_custom_report(user_id, start_date, end_date):
    try:
        c.execute("SELECT SUM(amount) FROM transactions WHERE user_id = ? AND transaction_type = 'income' AND date BETWEEN ? AND ?", (user_id, start_date, end_date))
        income = c.fetchone()[0] or 0
        c.execute("SELECT SUM(amount) FROM transactions WHERE user_id = ? AND transaction_type = 'expense' AND date BETWEEN ? AND ?", (user_id, start_date, end_date))
        expenses = c.fetchone()[0] or 0
    except Exception as e:
        print(f"An error occurred while generating the custom report: {e}")
        return

    print(f"\n--- Report from {start_date} to {end_date} ---")
    print(f"Total Income: ${income:.2f}")
    print(f"Total Expenses: ${expenses:.2f}")
    print(f"Net Savings: ${income - expenses:.2f}")

def generate_yearly_summary(user_id, year):
    try:
        c.execute("SELECT SUM(amount) FROM transactions WHERE user_id = ? AND transaction_type = 'income' AND strftime('%Y', date) = ?", (user_id, year))
        income = c.fetchone()[0] or 0
        c.execute("SELECT SUM(amount) FROM transactions WHERE user_id = ? AND transaction_type = 'expense' AND strftime('%Y', date) = ?", (user_id, year))
        expenses = c.fetchone()[0] or 0
    except Exception as e:
        print(f"An error occurred while generating the yearly summary: {e}")
        return

    print(f"\n--- {year} Yearly Summary ---")
    print(f"Total Income: ${income:.2f}")
    print(f"Total Expenses: ${expenses:.2f}")
    print(f"Net Savings: ${income - expenses:.2f}")

# Data Visualization Functions
def plot_monthly_expenses(user_id, year):
    try:
        months = [f"{i:02}" for i in range(1, 13)]
        expenses = []
        for month in months:
            c.execute("SELECT SUM(amount) FROM transactions WHERE user_id = ? AND transaction_type = 'expense' AND strftime('%Y', date) = ? AND strftime('%m', date) = ?", (user_id, year, month))
            expense = c.fetchone()[0] or 0
            expenses.append(expense)

        plt.figure(figsize=(10, 6))
        plt.bar(months, expenses)
        plt.xlabel('Month')
        plt.ylabel('Expenses ($)')
        plt.title(f'Expenses by Month for {year}')
        plt.show()
    except Exception as e:
        print(f"An error occurred while plotting monthly expenses: {e}")

def plot_income_expense_trend(user_id):
    try:
        c.execute("SELECT date, SUM(CASE WHEN transaction_type = 'income' THEN amount ELSE 0 END) as income, SUM(CASE WHEN transaction_type = 'expense' THEN amount ELSE 0 END) as expense FROM transactions WHERE user_id = ? GROUP BY date ORDER BY date", (user_id,))
        data = c.fetchall()

        dates = [row[0] for row in data]
        incomes = [row[1] for row in data]
        expenses = [row[2] for row in data]

        plt.figure(figsize=(10, 6))
        plt.plot(dates, incomes, label='Income', marker='o')
        plt.plot(dates, expenses, label='Expenses', marker='o')
        plt.xlabel('Date')
        plt.ylabel('Amount ($)')
        plt.title('Income and Expenses Over Time')
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"An error occurred while plotting income and expenses: {e}")

def plot_income_sources(user_id):
    try:
        c.execute("SELECT category, SUM(amount) FROM transactions WHERE user_id = ? AND transaction_type = 'income' GROUP BY category", (user_id,))
        income_sources = c.fetchall()
        if income_sources:
            labels = [row[0] for row in income_sources]
            sizes = [row[1] for row in income_sources]

            plt.figure(figsize=(10, 6))
            plt.pie(sizes, labels=labels, autopct='%1.1f%%')
            plt.title('Income Sources Distribution')
            plt.show()
        else:
            print("No income data to show.")
    except Exception as e:
        print(f"An error occurred while plotting income sources: {e}")

def plot_monthly_income_vs_expenses(user_id, year):
    try:
        months = [f"{i:02}" for i in range(1, 13)]
        incomes = []
        expenses = []
        for month in months:
            c.execute("SELECT SUM(amount) FROM transactions WHERE user_id = ? AND transaction_type = 'income' AND strftime('%Y', date) = ? AND strftime('%m', date) = ?", (user_id, year, month))
            income = c.fetchone()[0] or 0
            incomes.append(income)

            c.execute("SELECT SUM(amount) FROM transactions WHERE user_id = ? AND transaction_type = 'expense' AND strftime('%Y', date) = ? AND strftime('%m', date) = ?", (user_id, year, month))
            expense = c.fetchone()[0] or 0
            expenses.append(expense)

        plt.figure(figsize=(10, 6))
        plt.bar(months, incomes, label='Income', color='green')
        plt.bar(months, expenses, bottom=incomes, label='Expenses', color='red')
        plt.xlabel('Month')
        plt.ylabel('Amount ($)')
        plt.title(f'Monthly Income vs. Expenses for {year}')
        plt.legend()
        plt.show()
    except Exception as e:
        print(f"An error occurred while plotting monthly income vs. expenses: {e}")

def plot_cumulative_savings(user_id):
    try:
        c.execute("SELECT date, SUM(CASE WHEN transaction_type = 'income' THEN amount ELSE -amount END) as net FROM transactions WHERE user_id = ? GROUP BY date ORDER BY date", (user_id,))
        data = c.fetchall()

        dates = [row[0] for row in data]
        cumulative_savings = []
        total = 0
        for row in data:
            total += row[1]
            cumulative_savings.append(total)

        plt.figure(figsize=(10, 6))
        plt.plot(dates, cumulative_savings, label='Cumulative Savings', color='blue', marker='o')
        plt.xlabel('Date')
        plt.ylabel('Cumulative Savings ($)')
        plt.title('Cumulative Savings Over Time')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"An error occurred while plotting cumulative savings: {e}")

def plot_transaction_amounts_histogram(user_id):
    try:
        c.execute("SELECT amount FROM transactions WHERE user_id = ?", (user_id,))
        amounts = [row[0] for row in c.fetchall()]

        plt.figure(figsize=(10, 6))
        plt.hist(amounts, bins=20, edgecolor='black')
        plt.xlabel('Transaction Amount ($)')
        plt.ylabel('Frequency')
        plt.title('Distribution of Transaction Amounts')
        plt.show()
    except Exception as e:
        print(f"An error occurred while plotting transaction amounts histogram: {e}")

def plot_category_spending_trend(user_id):
    try:
        c.execute("SELECT DISTINCT category FROM transactions WHERE user_id = ? AND transaction_type = 'expense'", (user_id,))
        categories = [row[0] for row in c.fetchall()]

        plt.figure(figsize=(10, 6))
        for category in categories:
            c.execute("SELECT date, SUM(amount) FROM transactions WHERE user_id = ? AND transaction_type = 'expense' AND category = ? GROUP BY date ORDER BY date", (user_id, category))
            data = c.fetchall()
            dates = [row[0] for row in data]
            amounts = [row[1] for row in data]
            plt.plot(dates, amounts, label=category, marker='o')

        plt.xlabel('Date')
        plt.ylabel('Spending ($)')
        plt.title('Spending Trend by Category Over Time')
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"An error occurred while plotting category spending trends: {e}")

def plot_transaction_amounts_by_category(user_id):
    try:
        c.execute("SELECT DISTINCT category FROM transactions WHERE user_id = ? AND transaction_type = 'expense'", (user_id,))
        categories = [row[0] for row in c.fetchall()]
        category_data = []

        for category in categories:
            c.execute("SELECT amount FROM transactions WHERE user_id = ? AND transaction_type = 'expense' AND category = ?", (user_id, category))
            amounts = [row[0] for row in c.fetchall()]
            category_data.append(amounts)

        plt.figure(figsize=(10, 6))
        plt.boxplot(category_data, labels=categories)
        plt.xlabel('Category')
        plt.ylabel('Transaction Amount ($)')
        plt.title('Transaction Amounts by Category')
        plt.show()
    except Exception as e:
        print(f"An error occurred while plotting transaction amounts by category: {e}")

if __name__ == "__main__":
    create_tables()
    show_login_window()
