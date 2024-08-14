import sqlite3

# Database setup
conn = sqlite3.connect('data/finance_manager.db')
c = conn.cursor()

def create_tables():
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE,
                  password TEXT)''')
    conn.commit()

def drop_and_recreate_transactions_table():
    c.execute("DROP TABLE IF EXISTS transactions")
    c.execute('''CREATE TABLE IF NOT EXISTS transactions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  date TEXT,
                  amount REAL,
                  category TEXT,
                  description TEXT,
                  transaction_type TEXT,
                  FOREIGN KEY(user_id) REFERENCES users(id))''')
    conn.commit()
