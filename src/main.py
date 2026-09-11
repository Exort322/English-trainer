from src.ui.main_window import MainWindow
from src.database import DatabaseManager


def main():
    # создаем/подключаемся к БД
    data = DatabaseManager()
    data.connect()
    data.create_tables()

    # Создаем экземпляр нашего приложения
    app = MainWindow()

    # Запускаем постоянный цикл обработки событий окна
    app.mainloop()


if __name__ == "__main__":
    main()
