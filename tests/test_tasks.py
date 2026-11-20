import storage
import tasks


def test_add_task():
    storage.tasks = []
    storage.next_task_id = 1

    task = tasks.add_task(
        "Подготовить отчёт",
        "Программирование",
        "25.11.2026",
    )

    assert task["id"] == 1
    assert task["name"] == "Подготовить отчёт"
    assert task["completed"] is False
    assert len(tasks.get_tasks()) == 1


def test_complete_task():
    storage.tasks = [
        {
            "id": 1,
            "name": "Отчёт",
            "subject": "Программирование",
            "due_date": "25.11.2026",
            "completed": False,
        }
    ]
    storage.next_task_id = 2

    result = tasks.complete_task(1)

    assert result is True
    assert storage.tasks[0]["completed"] is True


def test_complete_already_completed_task():
    storage.tasks = [
        {
            "id": 1,
            "name": "Отчёт",
            "subject": "Программирование",
            "due_date": "25.11.2026",
            "completed": True,
        }
    ]

    result = tasks.complete_task(1)

    assert result is False


def test_complete_nonexistent_task():
    storage.tasks = []

    result = tasks.complete_task(999)

    assert result is None
