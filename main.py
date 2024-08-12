import csv
import matplotlib.pyplot as plt
from models import Transaction

# Data handling functions
def add_transaction(transaction):
    with open('data/transactions.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([transaction.date, transaction.amount, transaction.category, transaction.description, transaction.transaction_type])

def view_transactions():
    print("Date       | Amount | Category     | Description        | Type")
    print("--------------------------------------------------------------")
    with open('data/transactions.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]}")

# CLI functions
def add_transaction_cli():
    date = input("Enter the date (YYYY-MM-DD): ")
    amount = float(input("Enter the amount: "))
    category = input("Enter the category: ")
    description = input("Enter a description: ")
    transaction_type = input("Is this an 'income' or 'expense'? ").lower()

    if transaction_type not in ['income', 'expense']:
        print("Invalid transaction type. Please enter 'income' or 'expense'.")
        return

    transaction = Transaction(date, amount, category, description, transaction_type)
    add_transaction(transaction)
    print("Transaction added successfully!")

def generate_report():
    income = 0
    expenses = 0
    with open('data/transactions.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[4] == 'income':
                income += float(row[1])
            elif row[4] == 'expense':
                expenses += float(row[1])

    print("\n--- Report ---")
    print(f"Total Income: ${income:.2f}")
    print(f"Total Expenses: ${expenses:.2f}")
    print(f"Net Savings: ${income - expenses:.2f}")

def plot_expenses_by_category():
    categories = {}
    with open('data/transactions.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[4] == 'expense':
                if row[2] in categories:
                    categories[row[2]] += float(row[1])
                else:
                    categories[row[2]] = float(row[1])

    labels = categories.keys()
    sizes = categories.values()

    plt.figure(figsize=(10, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%')
    plt.title('Expenses by Category')
    plt.show()

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
    main_menu()
