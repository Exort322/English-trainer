import sqlite3
import customtkinter as ctk
from random import choice


class TrainingFrame(ctk.CTkFrame):
    def __init__(self, master, selected_group, database_manager):
        super().__init__(master)
        self.master = master
        self.selected_group = selected_group
        self.data = database_manager

        # Загружаем слова
        self.words = self.load_words()

        # Списки для статистики
        self.correct_list = []
        self.wrong_list = []

        # Переменные для отслеживания состояния текущей карточки
        self.current_word = None
        self.current_translation = None
        self.is_flipped = False  # False = английский, True = русский

        # Отрисовываем интерфейс
        self.create_widgets()

        # Показываем первое слово, если список не пуст
        self.next_card()

    def load_words(self):
        """Безопасно загружает слова с учетом выбора группы 'All'"""
        self.data.connect()
        try:
            if self.selected_group == "All":
                rows = self.data.cur.execute("SELECT english FROM words").fetchall()
            else:
                box_id = self.data.cur.execute("SELECT id FROM box WHERE name=?", (self.selected_group,)).fetchone()[0]
                rows = self.data.cur.execute("SELECT english FROM words WHERE box_id=?", (box_id,)).fetchall()
            return [i[0] for i in rows]
        except (sqlite3.Error, TypeError):
            return []
        finally:
            self.data.close()

    def get_translation(self, word):
        """Получает перевод слова из БД"""
        if not word:
            return ""
        self.data.connect()
        try:
            res = self.data.cur.execute("SELECT russian FROM words WHERE english=?", (word,)).fetchone()
            return res[0] if res else "Перевод не найден"
        except sqlite3.Error:
            return "Ошибка БД"
        finally:
            self.data.close()

    def next_card(self):
        """Загружает следующее слово или завершает тренировку"""
        if not self.words:
            self.show_results()
            return

        self.is_flipped = False
        self.current_word = choice(self.words)
        self.words.remove(self.current_word)
        self.current_translation = self.get_translation(self.current_word)

        # Сбрасываем текст карточки на английское слово
        self.word_label.configure(text=self.current_word, text_color="white")

    def flip_card(self, event=None):
        """Переворачивает карточку (меняет текст английский/русский)"""
        if not self.current_word:
            return

        if self.is_flipped:
            self.word_label.configure(text=self.current_word, text_color="white")
            self.is_flipped = False
        else:
            self.word_label.configure(text=self.current_translation, text_color="#2ECC71")
            self.is_flipped = True

    def mark_correct(self):
        """Обработка кнопки 'Знаю'"""
        if self.current_word:
            self.correct_list.append(self.current_word)
            self.next_card()

    def mark_wrong(self):
        """Обработка кнопки 'Не помню'"""
        if self.current_word:
            self.wrong_list.append(self.current_word)
            self.next_card()

    def show_results(self):
        """Скрывает управление и показывает результаты тренировки"""
        self.current_word = None

        # Скрываем кнопки управления
        self.control_panel.pack_forget()
        self.tip_label.pack_forget()

        # Меняем текст на карточке на финальный счет
        total = len(self.correct_list) + len(self.wrong_list)
        if total == 0:
            result_text = "В этой группе\nнет слов ¯\\_(ツ)_/¯"
        else:
            result_text = f"Тренировка окончена!\n\nИзучено: {len(self.correct_list)} из {total} ✅"

        self.word_label.configure(text=result_text, font=ctk.CTkFont(size=20, weight="bold"))

    def create_widgets(self):
        # Кнопка Назад
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

        # Карточка (CTkFrame)
        self.card = ctk.CTkFrame(self, width=400, height=220, fg_color="#2B2B2B", cursor="hand2")
        self.card.pack(pady=10)
        self.card.pack_propagate(False)

        # Привязываем клик по карточке к методу переворота
        self.card.bind("<Button-1>", self.flip_card)

        # Текст внутри карточки
        self.word_label = ctk.CTkLabel(
            self.card,
            text="",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        self.word_label.pack(expand=True)
        # Чтобы клик по самому тексту тоже переворачивал карточку:
        self.word_label.bind("<Button-1>", self.flip_card)

        # Инструкция
        self.tip_label = ctk.CTkLabel(
            self,
            text="Нажмите на карточку, чтобы перевернуть",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.tip_label.pack(pady=5)

        # Панель управления
        self.control_panel = ctk.CTkFrame(self, fg_color="transparent")
        self.control_panel.pack(pady=10)

        wrong_btn = ctk.CTkButton(
            self.control_panel,
            text="❌ Не помню",
            fg_color="#C0392B",
            hover_color="#962D22",
            width=120,
            command=self.mark_wrong
        )
        wrong_btn.pack(side="left", padx=10)

        correct_btn = ctk.CTkButton(
            self.control_panel,
            text="✅ Знаю",
            fg_color="#27AE60",
            hover_color="#1E8449",
            width=120,
            command=self.mark_correct
        )
        correct_btn.pack(side="left", padx=10)
