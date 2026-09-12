import customtkinter as ctk
from src.database import DatabaseManager

# Устанавливаем общую тему приложения
ctk.set_appearance_mode("dark")  # Варианты: "dark", "light", "system"
ctk.set_default_color_theme("blue")  # Варианты темы: "blue", "green", "dark-blue"


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Настройки главного окна
        self.title("Flashcards Trainer")
        self.geometry("600x500")
        self.resizable(False, False)  # Запретим менять размер для идеального сохранения верстки

        # Текущий контейнер для активного экрана
        self.current_frame = None

        # Сразу запускаем экран главного меню
        self.show_menu_frame()
        # БД
        self.data = DatabaseManager()

    def clear_current_frame(self):
        """Очищает окно перед отрисовкой нового экрана"""
        if self.current_frame is not None:
            self.current_frame.destroy()

    def show_menu_frame(self):
        """Экран главного меню приложения"""
        self.clear_current_frame()

        self.current_frame = ctk.CTkFrame(self)
        self.current_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Заголовок
        title_label = ctk.CTkLabel(
            self.current_frame,
            text="Выучи английские слова! 🚀",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(40, 30))

        # Кнопка: Режим Карточек
        cards_btn = ctk.CTkButton(
            self.current_frame,
            text="Режим: Карточки",
            height=45,
            width=250,
            font=ctk.CTkFont(size=16),
            command=self.show_cards_frame  # Действие по клику
        )
        cards_btn.pack(pady=10)

        # Кнопка: Добавить новое слово
        add_word_btn = ctk.CTkButton(
            self.current_frame,
            text="Добавить слова в базу",
            height=45,
            width=250,
            font=ctk.CTkFont(size=16),
            fg_color="transparent",  # Делаем кнопку контурной
            border_width=2,
            command=lambda: self.add_word_frame()
        )
        add_word_btn.pack(pady=10)

    def show_cards_frame(self):
        """Экран тренировки карточек"""
        self.clear_current_frame()

        self.current_frame = ctk.CTkFrame(self)
        self.current_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Кнопка Назад в меню
        back_btn = ctk.CTkButton(
            self.current_frame,
            text="⬅ Меню",
            width=80,
            command=self.show_menu_frame
        )
        back_btn.pack(anchor="w", padx=10, pady=10)

        # Сама интерактивная карточка (виджет-плашка)
        # Для имитации объема зададим чуть другой цвет фона
        card = ctk.CTkFrame(self.current_frame, width=400, height=220, fg_color="#2B2B2B")
        card.pack(pady=20)
        card.pack_propagate(False)  # Запрещаем карточке сжиматься под размер текста

        # Текст внутри карточки (для примера)
        word_label = ctk.CTkLabel(
            card,
            text="Developer",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        word_label.pack(expand=True)

        # Инструкция для пользователя
        tip_label = ctk.CTkLabel(
            self.current_frame,
            text="Нажмите на карточку, чтобы перевернуть",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        tip_label.pack(pady=5)

        # Панель для кнопок управления («Знаю» / «Не знаю»)
        control_panel = ctk.CTkFrame(self.current_frame, fg_color="transparent")
        control_panel.pack(pady=10)

        wrong_btn = ctk.CTkButton(control_panel, text="❌ Не помню", fg_color="#C0392B", hover_color="#962D22",
                                  width=120)
        wrong_btn.pack(side="left", padx=10)

        correct_btn = ctk.CTkButton(control_panel, text="✅ Знаю", fg_color="#27AE60", hover_color="#1E8449", width=120)
        correct_btn.pack(side="left", padx=10)

    def add_word_frame(self):
        self.clear_current_frame()

        self.current_frame = ctk.CTkFrame(self)
        self.current_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Кнопка Назад в меню
        back_btn = ctk.CTkButton(
            self.current_frame,
            text="⬅ Меню",
            width=80,
            command=self.show_menu_frame
        )
        back_btn.pack(anchor="w", padx=10, pady=10)

        # Заголовок экрана
        title_label = ctk.CTkLabel(
            self.current_frame,
            text="Добавление нового слова 📝",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=(0, 20))

        # Поле: Слово
        word_label = ctk.CTkLabel(self.current_frame, text="Слово (на английском):", font=ctk.CTkFont(size=14))
        word_label.pack(anchor="w", padx=130, pady=(5, 2))
        self.word_entry = ctk.CTkEntry(self.current_frame, width=300, placeholder_text="Word")
        self.word_entry.pack(pady=(0, 10))

        # Поле: Перевод
        trans_label = ctk.CTkLabel(self.current_frame, text="Перевод (на русском):", font=ctk.CTkFont(size=14))
        trans_label.pack(anchor="w", padx=130, pady=(5, 2))
        self.trans_entry = ctk.CTkEntry(self.current_frame, width=300, placeholder_text="Перевод")
        self.trans_entry.pack(pady=(0, 10))

        # Выбор группы (ComboBox)
        group_label = ctk.CTkLabel(self.current_frame, text="Выберите группу слова:", font=ctk.CTkFont(size=14))
        group_label.pack(anchor="w", padx=130, pady=(5, 2))

        # Контейнер для выпадающего списка и кнопки добавления группы
        group_inner_frame = ctk.CTkFrame(self.current_frame, fg_color="transparent")
        group_inner_frame.pack(pady=(0, 25))

        # подключаюсь к бд
        self.data.connect()
        # беру список групп из БД
        self.groups_list = self.data.cur.execute("SELECT name FROM box").fetchall()
        # привожу к нужному сиду
        self.groups_list = [i[0] for i in self.groups_list]
        self.data.close()
        # виджет - список групп
        self.group_combo = ctk.CTkComboBox(group_inner_frame, values=self.groups_list, width=180)
        self.group_combo.pack(side="left", padx=(0, 10))

        # Кнопка: Добавить группу
        add_group_btn = ctk.CTkButton(
            group_inner_frame,
            text="+ Группа",
            width=110,
            fg_color="transparent",
            border_width=1,
            command=self.add_new_group_dialog
        )
        add_group_btn.pack(side="left")

        # Кнопка: Сохранить слово
        save_btn = ctk.CTkButton(
            self.current_frame,
            text="Сохранить слово",
            height=40,
            width=300,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#27AE60",
            hover_color="#1E8449",
            command=self.save_word
        )
        save_btn.pack(pady=10)

    def add_new_group_dialog(self):
        """Всплывающее окно для добавления новой группы"""
        dialog = ctk.CTkInputDialog(text="Введите название новой группы:", title="Новая группа")
        new_group = dialog.get_input()

        if new_group and new_group.strip():
            new_group = new_group.strip()
            if new_group not in self.groups_list:
                # подключаюсь к бд
                self.data.connect()
                # добавляю новую группу в бд
                self.data.cur.execute(f'''
                                    INSERT INTO box (name) VALUES (?)
                                    ''', (new_group,))
                # закрываю и сохраняю бд
                #self.data.con.commit()
                #self.data.close()

                self.groups_list.append(new_group)
                self.group_combo.configure(values=self.groups_list)
                self.group_combo.set(new_group)  # Автоматически выбираем созданную группу

    def save_word(self):
        """Логика сохранения слова (пока просто вывод в консоль)"""
        word_eng = self.word_entry.get().strip()
        translation = self.trans_entry.get().strip()
        group = self.group_combo.get()

        if not word_eng or not translation:
            print("Ошибка: Заполните все поля!")
            return
        # подключение к бд
        self.data.connect()
        # забираю id групп из бд
        box_id = self.data.cur.execute("SELECT id FROM box WHERE name=?", (group,)).fetchone()[0]
        # добавление слова в бд
        self.data.cur.execute('''INSERT INTO words (english, russian, box_id) VALUES (?, ?, ?)''',
                              (word_eng, translation, box_id))
        self.data.con.commit()
        self.data.close()

        print(f"Сохранено: {word_eng} — {translation} [Группа: {group}]")

        # Очищаем поля ввода после успешного сохранения
        self.word_entry.delete(0, 'end')
        self.trans_entry.delete(0, 'end')
