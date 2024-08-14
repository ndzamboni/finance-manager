from finance_manager.database import create_tables, drop_and_recreate_transactions_table
from finance_manager.gui import show_login_window

if __name__ == "__main__":
    create_tables()
    drop_and_recreate_transactions_table()  # Ensure the transactions table is correctly set up
    show_login_window()
