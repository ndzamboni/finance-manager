import sqlite3
from models import Transaction
from datetime import datetime
import matplotlib.pyplot as plt

# Database setup
conn = sqlite3.connect('data/finance_manager.db')
c = conn.cursor()

def create_table():
    c.execute('''CREATE TABLE IF NOT EXISTS transactions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  date TEXT,
                  amount REAL,
                  category TEXT,
                  description TEXT,
                  transaction_type TEXT)''')
    conn.commit()

# Data handling functions
def add_transaction(transaction):
    try:
        c.execute("INSERT INTO transactions (date, amount, category, description, transaction_type) VALUES (?, ?, ?, ?, ?)",
                  (transaction.date, transaction.amount, transaction.category, transaction.description, transaction.transaction_type))
        conn.commit()
    except Exception as e:
        print(f"An error occurred while adding the transaction: {e}")

def view_transactions():
    try:
        c.execute("SELECT * FROM transactions")
        rows = c.fetchall()
        if rows:
            print("Date       | Amount | Category     | Description        | Type")
            print("--------------------------------------------------------------")
            for row in rows:
                print(f"{row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]}")
        else:
            print("No transactions found.")
    except Exception as e:
        print(f"An error occurred while viewing the transactions: {e}")

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

def add_transaction_cli():
    date = input("Enter the date (YYYY-MM-DD): ")
    if not validate_date(date):
        print("Invalid date format. Please use YYYY-MM-DD.")
        return

    amount = input("Enter the amount: ")
    if not validate_amount(amount):
        print("Invalid amount. Please enter a positive number.")
        return

    category = input("Enter the category: ")
    description = input("Enter a description: ")
    transaction_type = input("Is this an 'income' or 'expense'? ").lower()

    if transaction_type not in ['income', 'expense']:
        print("Invalid transaction type. Please enter 'income' or 'expense'.")
        return

    transaction = Transaction(date, float(amount), category, description, transaction_type)
    add_transaction(transaction)
    print("Transaction added successfully!")

def generate_report():
    try:
        c.execute("SELECT SUM(amount) FROM transactions WHERE transaction_type = 'income'")
        income = c.fetchone()[0] or 0
        c.execute("SELECT SUM(amount) FROM transactions WHERE transaction_type = 'expense'")
        expenses = c.fetchone()[0] or 0
    except Exception as e:
        print(f"An error occurred while generating the report: {e}")
        return

    print("\n--- Report ---")
    print(f"Total Income: ${income:.2f}")
    print(f"Total Expenses: ${expenses:.2f}")
    print(f"Net Savings: ${income - expenses:.2f}")

def plot_expenses_by_category():
    try:
        c.execute("SELECT category, SUM(amount) FROM transactions WHERE transaction_type = 'expense' GROUP BY category")
        categories = c.fetchall()
        if categories:
            labels = [row[0] for row in categories]
            sizes = [row[1] for row in categories]

            plt.figure(figsize=(10, 6))
            plt.pie(sizes, labels=labels, autopct='%1.1f%%')
            plt.title('Expenses by Category')
            plt.show()
        else:
            print("No expenses to show.")
    except Exception as e:
        print(f"An error occurred while generating the chart: {e}")

def main_menu():
    while True:
        print("\nFinance Manager")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Generate Report")
        print("4. Visualize Expenses")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_transaction_cli()
        elif choice == '2':
            view_transactions()
        elif choice == '3':
            generate_report()
        elif choice == '4':
            plot_expenses_by_category()
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    create_table()
    main_menu()
