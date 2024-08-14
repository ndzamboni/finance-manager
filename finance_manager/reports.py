from .database import c

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
