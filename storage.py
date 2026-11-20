import json
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
DATA_FILE = DATA_DIR / "tasks.json"

tasks = []
next_task_id = 1


def save_tasks():
    """Сохраняет задачи в JSON-файл."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    data = {
        "tasks": tasks,
        "next_task_id": next_task_id,
    }

    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def load_tasks():
    """Загружает задачи из JSON-файла."""
    global tasks, next_task_id

    if not DATA_FILE.exists():
        tasks = []
        next_task_id = 1
        return

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

        loaded_tasks = data["tasks"]
        loaded_next_id = data["next_task_id"]

        if not isinstance(loaded_tasks, list):
            raise TypeError("Некорректный формат списка задач.")

        if not isinstance(loaded_next_id, int) or loaded_next_id < 1:
            raise ValueError("Некорректный идентификатор следующей задачи.")

        tasks = loaded_tasks
        next_task_id = loaded_next_id

    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        raise ValueError(f"Не удалось загрузить данные: {error}") from error
    except OSError as error:
        raise OSError(f"Ошибка чтения файла данных: {error}") from error
