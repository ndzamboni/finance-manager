import matplotlib.pyplot as plt
from .database import c

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
