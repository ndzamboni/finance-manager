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
            return rows  # Return the fetched rows
        else:
            print("No transactions found.")
            return []  # Return an empty list if no transactions found
    except Exception as e:
        print(f"An error occurred while viewing the transactions: {e}")
        return []

def get_transaction_by_id(user_id, transaction_id):
    try:
        c.execute("SELECT * FROM transactions WHERE id = ? AND user_id = ?", (transaction_id, user_id))
        return c.fetchone()
    except Exception as e:
        print(f"An error occurred while retrieving the transaction: {e}")
        return None

def edit_transaction(user_id, transaction_id, new_date, new_amount, new_category, new_description, new_transaction_type):
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
