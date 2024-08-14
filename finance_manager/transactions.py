from .database import c, conn

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
