from datetime import datetime

import tasks


def show_help():
    """Показывает список доступных команд."""
    print("\nДоступные команды:")
    print("add  - добавить задачу")
    print("list - показать все задачи")
    print("done - отметить задачу выполненной")
    print("help - показать справку")
    print("exit - завершить программу")


def handle_add():
    """Запрашивает данные и добавляет новую задачу."""
    name = input("Название задачи: ").strip()
    if not name:
        print("Ошибка: название не может быть пустым.")
        return

    subject = input("Предмет: ").strip()
    if not subject:
        print("Ошибка: предмет не может быть пустым.")
        return

    due_date = input("Срок выполнения (ДД.ММ.ГГГГ): ").strip()

    try:
        datetime.strptime(due_date, "%d.%m.%Y")
    except ValueError:
        print("Ошибка: введите дату в формате ДД.ММ.ГГГГ.")
        return

    task = tasks.add_task(name, subject, due_date)
    print(f"Задача добавлена. Её ID: {task['id']}")


def handle_list():
    """Показывает все задачи и их статусы."""
    all_tasks = tasks.get_tasks()

    if not all_tasks:
        print("Список задач пуст.")
        return

    print("\nВаши задачи:")
    for task in all_tasks:
        status = "Выполнено" if task["completed"] else "В процессе"
        print(
            f"ID: {task['id']} | {task['name']} | "
            f"Предмет: {task['subject']} | "
            f"Срок: {task['due_date']} | Статус: {status}"
        )


def handle_done():
    """Отмечает задачу выполненной по её ID."""
    task_id_text = input("Введите ID задачи: ").strip()

    try:
        task_id = int(task_id_text)
    except ValueError:
        print("Ошибка: ID должен быть целым числом.")
        return

    result = tasks.complete_task(task_id)

    if result is True:
        print("Задача отмечена как выполненная.")
    elif result is False:
        print("Эта задача уже выполнена.")
    else:
        print("Задача с таким ID не найдена.")


def process_command(command):
    """Обрабатывает введённую пользователем команду."""
    if command == "add":
        handle_add()
    elif command == "list":
        handle_list()
    elif command == "done":
        handle_done()
    elif command == "help":
        show_help()
    elif command == "exit":
        return False
    else:
        print("Неизвестная команда. Введите help для просмотра справки.")

    return True
