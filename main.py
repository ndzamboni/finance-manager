from finance_manager.database import create_tables
from finance_manager.gui import show_login_window
from finance_manager.transactions import add_transaction, view_transactions, get_transaction_by_id, edit_transaction, delete_transaction
from finance_manager.models import Transaction  # Keep only the Transaction import

if __name__ == "__main__":
    create_tables()  # Only create tables if they don't exist
    show_login_window()
