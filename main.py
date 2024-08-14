from finance_manager.database import create_tables
from finance_manager.gui import show_login_window

if __name__ == "__main__":
    create_tables()  # Only create tables if they don't exist
    show_login_window()
