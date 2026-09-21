import sqlite3

import customtkinter as ctk
from random import choice

class TrainingFrame(ctk.CTkFrame):
    def __init__(self, master, selected_group, database_manager):
        # Инициализируем базовый фрейм, привязывая его к главному окну
        super().__init__(master)
        self.master = master
        self.selected_group = selected_group

        self.data = database_manager
        self.data.connect()
        self.box_id = self.data.cur.execute("SELECT id FROM box WHERE name=?", (self.selected_group,)).fetchone()[0]
        # забираем из бд слова  выбраной группы
        self.words = self.data.cur.execute(f"SELECT english FROM words WHERE box_id=?", (self.box_id,)).fetchall()
        self.words = [i[0] for i in self.words]
        print(self.words)
        self.data.close()

        # список правильных/неправильных ответов
        self.correct_list, self.wrong_list = list(), list()

        # Отрисовываем интерфейс тренировки
        self.create_widgets()
        print(self.get_translation("qwe"))

    def get_card(self):
        # добавить проверку не пустой ли список
        word = choice(self.words)
        self.words.remove(word)
        return word

    def get_translation(self, word):
        try:
            self.data.connect()
            translation = self.data.cur.execute("SELECT russian FROM words WHERE english=?", (word,)).fetchone()[0]
            self.data.close()
            return translation
        except (sqlite3.Error, TypeError) as e:
            self.data.close()
            print(f"Не найден перевод {word}")


    def create_widgets(self):
        # Кнопка Назад (вызывает метод главного окна)
        back_btn = ctk.CTkButton(
            self,
            text="⬅ К выбору",
            width=80,
            command=self.master.show_select_group_frame
        )
        back_btn.pack(anchor="w", padx=10, pady=10)

        # Имя текущей группы
        group_label = ctk.CTkLabel(
            self,
            text=f"Группа: {self.selected_group}",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="gray"
        )
        group_label.pack(pady=(0, 10))

        # Карточка
        self.card = ctk.CTkFrame(self, width=400, height=220, fg_color="#2B2B2B")
        self.card.pack(pady=10)
        self.card.pack_propagate(False)

        # Текст внутри карточки
        self.word_label = ctk.CTkLabel(
            self.card,
            text="Developer",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        self.word_label.pack(expand=True)

        # Инструкция
        tip_label = ctk.CTkLabel(
            self,
            text="Нажмите на карточку, чтобы перевернуть",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        tip_label.pack(pady=5)

        # Панель управления
        control_panel = ctk.CTkFrame(self, fg_color="transparent")
        control_panel.pack(pady=10)

        wrong_btn = ctk.CTkButton(control_panel, text="❌ Не помню", fg_color="#C0392B", hover_color="#962D22", width=120)
        wrong_btn.pack(side="left", padx=10)

        correct_btn = ctk.CTkButton(control_panel, text="✅ Знаю", fg_color="#27AE60", hover_color="#1E8449", width=120)
        correct_btn.pack(side="left", padx=10)
