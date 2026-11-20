import storage


def add_task(name, subject, due_date):
    """Добавляет новую задачу."""
    task = {
        "id": storage.next_task_id,
        "name": name,
        "subject": subject,
        "due_date": due_date,
        "completed": False,
    }

    storage.tasks.append(task)
    storage.next_task_id += 1

    return task


def get_tasks():
    """Возвращает список всех задач."""
    return storage.tasks


def complete_task(task_id):
    """Отмечает задачу как выполненную."""
    for task in storage.tasks:
        if task["id"] == task_id:
            if task["completed"]:
                return False

            task["completed"] = True
            return True

    return None
