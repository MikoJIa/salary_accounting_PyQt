import hashlib
import os
import sqlite3
from pathlib import Path


class DataBase:

    def __init__(self):
        self.db_path = Path(__file__).parent / 'salary.db'
        self.initialize_db()
        self.init_salary_table()
        self.init_registration_requests()
        self.create_default_admin()
        self.get_pending()
        self.get_all_users()

    def initialize_db(self):
        conn = sqlite3.connect("user.db")
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        login TEXT UNIQUE NOT NULL,
        password text NOT NULL,
        admin INTEGER DEFAULT 0, 
        create_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP)
        """)

        cursor.execute("""CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        ip_address text NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id))
        """)

    def init_registration_requests(self):
        conn = sqlite3.connect("requests.db")
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS registration_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        login TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'pending', -- 'pending', 'approved', 'rejected',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
        )
        """)
        conn.commit()
        conn.close()

    def create_registration_request(self, login, password):
        login = login.strip()
        password = password.strip()
        if not login or not password:
            return False, "Логин и пароль должны быть заполнены!"
        if self.check_user(login):
            return False, "Пользователь с таким логином уже существует!!!"

        try:
            conn = sqlite3.connect("requests.db")
            cursor = conn.cursor()
            cursor.execute("""
            SELECT id FROM registration_requests WHERE login = ? AND status = 'pending'
            """, (login,))
            if cursor.fetchone():
                conn.close()
                return False, "Такая заявка уже есть!!!"
            pass_hash = self.hashing_password(password)
            cursor.execute("""
            INSERT INTO registration_requests (login, password) VALUES (?, ?)
            """, (login, pass_hash))
            conn.commit()
            conn.close()
            return True, "Заявка перинята"
        except Exception as e:
            return False, str(e)

    def create_default_admin(self):
        # создание администратора admin/1
        if not self.check_user('admin'):
            conn = sqlite3.connect("user.db")
            try:
                cursor = conn.cursor()
                pass_hash = self.hashing_password('1')
                print(pass_hash)
                cursor.execute("""
                INSERT OR IGNORE INTO users (login, password, admin) VALUES (?, ?, ?)
                """, ('admin', pass_hash, 1))
                conn.commit()
            finally:
                conn.close()

            conn = sqlite3.connect("user.db")
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT id, login, admin FROM users")
                for row in cursor.fetchall():
                    print("user:", row)
            finally:
                conn.close()

    def init_salary_table(self):
        conn = sqlite3.connect('salary.db')
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS salary_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER NOT NULL,
        fio TEXT NOT NULL,
        total_hours REAL,
        price_one_hour REAL,
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
        return hashlib.sha256(password.encode()).hexdigest()

    def approve_registration(self, request_id):
        conn = sqlite3.connect("requests.db")
        conn_users = sqlite3.connect("user.db")
        cursor = conn.cursor()
        try:
            cursor.execute("""
            SELECT login, password FROM registration_requests WHERE id = ? AND status = 'pending'
            """, (request_id,))
            request = cursor.fetchone()
            if not request:
                return False, "Заявка не найдена!!!"
            login, password = request

            cursor_users = conn_users.cursor()
            cursor_users.execute("""
            INSERT INTO users (login, password) VALUES (?, ?)
            """, (login, password))
            cursor.execute(
                "UPDATE registration_requests SET status = 'approved' WHERE id = ?",
                (request_id,))
            conn.commit()
            conn_users.commit()
            return True, f"Пользователь '{login}' одобрен!"
        except Exception as e:
            conn.rollback()
            conn_users.rollback()
            return False, str(e)
        finally:
            conn.close()
            conn_users.close()

    def reject_registration(self, request_id):
        """Отклоняет заявку"""
        try:
            conn = sqlite3.connect("requests.db")
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE registration_requests SET status = 'rejected' WHERE id = ?",
                (request_id,)
            )
            conn.commit()
            conn.close()
            return True, "Заявка отклонена!"
        except Exception as e:
            return False, str(e)

    def check_user(self, login):
        try:
            conn = sqlite3.connect("user.db")
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
            conn = sqlite3.connect('user.db')
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
                conn = sqlite3.connect("user.db")
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

    def is_admin(self, login):
        """проверка пользователя на администратора"""
        conn = sqlite3.connect("user.db")
        cursor = conn.cursor()
        cursor.execute("SELECT admin FROM users WHERE login = ?", (login,))
        row = cursor.fetchone()
        conn.close()
        return row is not None and row[0] == 1

    def get_pending(self):
        conn = sqlite3.connect("requests.db")
        cursor = conn.cursor()
        cursor.execute("""
        SELECT id, login, created_at FROM registration_requests WHERE status = 'pending' ORDER BY created_at DESC
        """)
        rows = cursor.fetchall()
        conn.close()
        return rows

    def get_all_users(self):
        conn = sqlite3.connect("user.db")
        cursor = conn.cursor()
        cursor.execute("""
             SELECT id, login, admin, create_at
             FROM users
             ORDER BY create_at DESC
         """)
        rows = cursor.fetchall()
        conn.close()
        return rows

    def delete_user(self, user_id):
        try:
            conn = sqlite3.connect("user.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = ? AND login != 'admin'", (user_id,))
            conn.commit()
            conn.close()
            return True, "Пользователь удалён."
        except Exception as e:
            return False, str(e)