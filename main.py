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

# Advanced Reporting Functions
def generate_monthly_report(year, month):
    try:
        c.execute("SELECT SUM(amount) FROM transactions WHERE transaction_type = 'income' AND strftime('%Y', date) = ? AND strftime('%m', date) = ?", (year, month))
        income = c.fetchone()[0] or 0
        c.execute("SELECT SUM(amount) FROM transactions WHERE transaction_type = 'expense' AND strftime('%Y', date) = ? AND strftime('%m', date) = ?", (year, month))
        expenses = c.fetchone()[0] or 0
    except Exception as e:
        print(f"An error occurred while generating the monthly report: {e}")
        return

    print(f"\n--- {month}-{year} Report ---")
    print(f"Total Income: ${income:.2f}")
    print(f"Total Expenses: ${expenses:.2f}")
    print(f"Net Savings: ${income - expenses:.2f}")

def generate_custom_report(start_date, end_date):
    try:
        c.execute("SELECT SUM(amount) FROM transactions WHERE transaction_type = 'income' AND date BETWEEN ? AND ?", (start_date, end_date))
        income = c.fetchone()[0] or 0
        c.execute("SELECT SUM(amount) FROM transactions WHERE transaction_type = 'expense' AND date BETWEEN ? AND ?", (start_date, end_date))
        expenses = c.fetchone()[0] or 0
    except Exception as e:
        print(f"An error occurred while generating the custom report: {e}")
        return

    print(f"\n--- Report from {start_date} to {end_date} ---")
    print(f"Total Income: ${income:.2f}")
    print(f"Total Expenses: ${expenses:.2f}")
    print(f"Net Savings: ${income - expenses:.2f}")

def generate_yearly_summary(year):
    try:
        c.execute("SELECT SUM(amount) FROM transactions WHERE transaction_type = 'income' AND strftime('%Y', date) = ?", (year,))
        income = c.fetchone()[0] or 0
        c.execute("SELECT SUM(amount) FROM transactions WHERE transaction_type = 'expense' AND strftime('%Y', date) = ?", (year,))
        expenses = c.fetchone()[0] or 0
    except Exception as e:
        print(f"An error occurred while generating the yearly summary: {e}")
        return

    print(f"\n--- {year} Yearly Summary ---")
    print(f"Total Income: ${income:.2f}")
    print(f"Total Expenses: ${expenses:.2f}")
    print(f"Net Savings: ${income - expenses:.2f}")

# Data Visualization Functions
def plot_monthly_expenses(year):
    try:
        months = [f"{i:02}" for i in range(1, 13)]
        expenses = []
        for month in months:
            c.execute("SELECT SUM(amount) FROM transactions WHERE transaction_type = 'expense' AND strftime('%Y', date) = ? AND strftime('%m', date) = ?", (year, month))
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

def plot_income_expense_trend():
    try:
        c.execute("SELECT date, SUM(CASE WHEN transaction_type = 'income' THEN amount ELSE 0 END) as income, SUM(CASE WHEN transaction_type = 'expense' THEN amount ELSE 0 END) as expense FROM transactions GROUP BY date ORDER BY date")
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

def plot_income_sources():
    try:
        c.execute("SELECT category, SUM(amount) FROM transactions WHERE transaction_type = 'income' GROUP BY category")
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

def plot_monthly_income_vs_expenses(year):
    try:
        months = [f"{i:02}" for i in range(1, 13)]
        incomes = []
        expenses = []
        for month in months:
            c.execute("SELECT SUM(amount) FROM transactions WHERE transaction_type = 'income' AND strftime('%Y', date) = ? AND strftime('%m', date) = ?", (year, month))
            income = c.fetchone()[0] or 0
            incomes.append(income)

            c.execute("SELECT SUM(amount) FROM transactions WHERE transaction_type = 'expense' AND strftime('%Y', date) = ? AND strftime('%m', date) = ?", (year, month))
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

def plot_cumulative_savings():
    try:
        c.execute("SELECT date, SUM(CASE WHEN transaction_type = 'income' THEN amount ELSE -amount END) as net FROM transactions GROUP BY date ORDER BY date")
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

def plot_transaction_amounts_histogram():
    try:
        c.execute("SELECT amount FROM transactions")
        amounts = [row[0] for row in c.fetchall()]

        plt.figure(figsize=(10, 6))
        plt.hist(amounts, bins=20, edgecolor='black')
        plt.xlabel('Transaction Amount ($)')
        plt.ylabel('Frequency')
        plt.title('Distribution of Transaction Amounts')
        plt.show()
    except Exception as e:
        print(f"An error occurred while plotting transaction amounts histogram: {e}")

def plot_category_spending_trend():
    try:
        c.execute("SELECT DISTINCT category FROM transactions WHERE transaction_type = 'expense'")
        categories = [row[0] for row in c.fetchall()]

        plt.figure(figsize=(10, 6))
        for category in categories:
            c.execute("SELECT date, SUM(amount) FROM transactions WHERE transaction_type = 'expense' AND category = ? GROUP BY date ORDER BY date", (category,))
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

def plot_transaction_amounts_by_category():
    try:
        c.execute("SELECT DISTINCT category FROM transactions WHERE transaction_type = 'expense'")
        categories = [row[0] for row in c.fetchall()]
        category_data = []

        for category in categories:
            c.execute("SELECT amount FROM transactions WHERE transaction_type = 'expense' AND category = ?", (category,))
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

# Main Menu
def main_menu():
    while True:
        print("\nFinance Manager")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Generate Report")
        print("4. Visualize Data")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_transaction_cli()
        elif choice == '2':
            view_transactions()
        elif choice == '3':
            print("\n1. Monthly Report")
            print("2. Custom Date Range Report")
            print("3. Yearly Summary")
            report_choice = input("Enter your choice: ")
            if report_choice == '1':
                year = input("Enter year (YYYY): ")
                month = input("Enter month (MM): ")
                generate_monthly_report(year, month)
            elif report_choice == '2':
                start_date = input("Enter start date (YYYY-MM-DD): ")
                end_date = input("Enter end date (YYYY-MM-DD): ")
                generate_custom_report(start_date, end_date)
            elif report_choice == '3':
                year = input("Enter year (YYYY): ")
                generate_yearly_summary(year)
            else:
                print("Invalid choice.")
        elif choice == '4':
            print("\n1. Monthly Expenses Bar Chart")
            print("2. Income and Expenses Over Time Line Graph")
            print("3. Pie Chart of Income Sources")
            print("4. Stacked Bar Chart of Monthly Income vs. Expenses")
            print("5. Cumulative Savings Over Time")
            print("6. Histogram of Transaction Amounts")
            print("7. Category-Wise Spending Over Time")
            print("8. Box Plot of Transaction Amounts by Category")
            visualize_choice = input("Enter your choice: ")
            if visualize_choice == '1':
                year = input("Enter year (YYYY): ")
                plot_monthly_expenses(year)
            elif visualize_choice == '2':
                plot_income_expense_trend()
            elif visualize_choice == '3':
                plot_income_sources()
            elif visualize_choice == '4':
                year = input("Enter year (YYYY): ")
                plot_monthly_income_vs_expenses(year)
            elif visualize_choice == '5':
                plot_cumulative_savings()
            elif visualize_choice == '6':
                plot_transaction_amounts_histogram()
            elif visualize_choice == '7':
                plot_category_spending_trend()
            elif visualize_choice == '8':
                plot_transaction_amounts_by_category()
            else:
                print("Invalid choice.")
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    create_table()
    main_menu()
