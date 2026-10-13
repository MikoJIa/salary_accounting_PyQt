import hashlib
import os
import sqlite3
from pathlib import Path


class DataBase:

    def __init__(self):
        self.db_path = Path(__file__).parent / 'salary.db'
        #self.initialize_db()
        #self.init_salary_table()

    def initialize_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        login TEXT UNIQUE NOT NULL,
        password text NOT NULL, 
        create_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP)
        """)

        cursor.execute("""CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        ip_address text NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id))
        """)

    def init_salary_table(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS salary_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER NOT NULL,
        fio TEXT NOT NULL,
        total_hours REAL NOT NULL,
        price_one_hour REAL NOT NULL,
        job_title TEXT NOT NULL,
        accrual REAL NOT NULL,
        vacation_pay REAL DEFAULT 0,
        remains REAL,
        record_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
        )
        """)
        conn.commit()
        conn.close()


    def hashing_password(self, password):
        salt_bytes = os.urandom(16)
        salt_hex = hashlib.sha256((password + salt_bytes).encode()).hexdigest()
        return salt_hex

    def check_user(self, login):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""SELECT id FROM users WHERE login = ?""", (login,))
            row = cursor.fetchone()
            conn.close()
            return row is not None
        except Exception as e:
            print(e)
            return False

    def verification(self, login, password):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            pass_encoding = self.hashing_password(password)
            cursor.execute(
                """SELECT id FROM users WHERE login = ? AND password = ?""",
                (login, pass_encoding)
            )
            row = cursor.fetchone()
            conn.close()
            return row is not None
        except Exception as e:
            print(e)
            return False

    def add_user(self, login, password):
        try:
            if self.check_user(login):
                return False, "Пользователь с таким логином существует!"
            else:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                pass_encoding = self.hashing_password(password)
                cursor.execute(
                    '''INSERT INTO users (login, password) VALUES (?, ?)''',
                    (login, pass_encoding)
                )
                conn.commit()
                conn.close()
                return True, "Пользователь успешно зарегистрирован!"
        except Exception as e:
            return False, str(e)