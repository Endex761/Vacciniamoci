from settings import SQLITE_FILE
import sqlite3
from sqlite3 import Error
from sqlite3.dbapi2 import IntegrityError

class Database:
    def __init__(self) -> None:
        self.db_file = SQLITE_FILE
        self.create_connection()

    def create_connection(self):
        conn = None
        try:
            conn = sqlite3.connect(self.db_file)
            self.conn = conn
        except Error as e:
            print(e)

    def close(self):
        if self.conn:
            self.conn.close()
        
    def create_table(self):
        create_users_table = "CREATE TABLE IF NOT EXISTS users ( chat_id integer PRIMARY KEY );"
        cur = self.conn.cursor()
        cur.execute(create_users_table)

    def add_user(self, chat_id) -> None:
        sql = "INSERT INTO users(chat_id) VALUES(?)"
        cur = self.conn.cursor()
        try: 
            cur.execute(sql, [chat_id])
            self.conn.commit()
        except IntegrityError as e:
            # print(e)
            pass

    def get_users(self) -> None:
        sql = "SELECT * FROM users"
        cur = self.conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        return rows

    def rem_user(self, chat_id):
        sql = "DELETE FROM users WHERE chat_id = ?"
        cur = self.conn.cursor()
        cur.execute(sql, [chat_id])
        self.conn.commit()