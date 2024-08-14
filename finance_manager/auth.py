import bcrypt
from .database import c, conn
import sqlite3


def register_user(username, password):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
        conn.commit()
        print("User registered successfully.")
    except sqlite3.IntegrityError:
        print("Username already exists. Please choose a different username.")

def login_user(username, password):
    c.execute("SELECT id, password FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    if result and bcrypt.checkpw(password.encode('utf-8'), result[1]):
        print("Login successful.")
        return result[0]
    else:
        print("Invalid username or password.")
        return None
