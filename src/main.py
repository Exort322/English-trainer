from src.ui.main_window import MainWindow


def main():
    # Создаем экземпляр нашего приложения
    app = MainWindow()

    # Запускаем постоянный цикл обработки событий окна
    app.mainloop()


if __name__ == "__main__":
    main()
