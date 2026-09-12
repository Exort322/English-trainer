import sqlite3
import sqlite3 as sq
import os


class DatabaseManager:
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.db_path = os.path.join(base_dir, 'data', 'words.db')  # путь к db

    def connect(self):
        try:
            self.con = sq.connect(database=self.db_path)
            self.cur = self.con.cursor()
            print(f"Успешное подключение к БД: {self.db_path}")
        except sqlite3.Error as e:
            print(f"Ошибка при подключении к базе данных: {e}")

    def close(self):
        if self.con:
            self.con.close()
            print("БД закрыта")

    def create_tables(self):
        """Создает таблицу для слов, если её еще нет"""
        self.connect()

        # Создаем таблицу слов
        # english - слово на английском
        # russian - перевод
        # box - номер коробки (нужен для алгоритма повторений, например Leitner System)
        self.cur.execute('''
                    CREATE TABLE IF NOT EXISTS box (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL UNIQUE 
                        )
                ''')
        self.cur.execute('''
        INSERT INTO box (id, name) VALUES (1, "Unsorted")
        ''')

        self.cur.execute('''
                    CREATE TABLE IF NOT EXISTS words (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        english TEXT NOT NULL UNIQUE,
                        russian TEXT NOT NULL,
                        box_id INTEGER DEFAULT 1,
                        FOREIGN KEY (box_id) REFERENCES box(id) ON DELETE SET DEFAULT
                        )
                ''')

        self.con.commit()
        self.close()
