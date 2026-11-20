import commands
import storage


def main():
    """Запускает StudyMate AI."""
    print("Добро пожаловать в StudyMate AI!")
    print("Ваш помощник для управления учебными задачами.")

    try:
        storage.load_tasks()
        print(f"Загружено задач: {len(storage.tasks)}")
    except (OSError, ValueError) as error:
        print(f"Ошибка загрузки данных: {error}")
        return
    commands.show_help()

    running = True

    while running:
        user_command = input("\nВведите команду: ").strip().lower()
        running = commands.process_command(user_command)

    print("Работа программы завершена. До свидания!")


if __name__ == "__main__":
    main()
