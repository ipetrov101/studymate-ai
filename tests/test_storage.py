import json

import pytest

import storage


def test_load_tasks_when_file_does_not_exist(tmp_path, monkeypatch):
    data_file = tmp_path / "tasks.json"
    monkeypatch.setattr(storage, "DATA_FILE", data_file)

    storage.tasks = []
    storage.next_task_id = 5

    storage.load_tasks()

    assert storage.tasks == []
    assert storage.next_task_id == 1


def test_save_and_load_tasks(tmp_path, monkeypatch):
    data_file = tmp_path / "tasks.json"
    monkeypatch.setattr(storage, "DATA_FILE", data_file)
    monkeypatch.setattr(storage, "DATA_DIR", tmp_path)

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

    storage.save_tasks()
    storage.tasks = []
    storage.next_task_id = 1
    storage.load_tasks()

    assert len(storage.tasks) == 1
    assert storage.tasks[0]["name"] == "Отчёт"
    assert storage.next_task_id == 2


def test_load_tasks_with_invalid_json(tmp_path, monkeypatch):
    data_file = tmp_path / "tasks.json"
    monkeypatch.setattr(storage, "DATA_FILE", data_file)

    data_file.write_text("{invalid json}", encoding="utf-8")

    try:
        storage.load_tasks()
    except ValueError as error:
        assert "Не удалось загрузить данные" in str(error)
    else:
        raise AssertionError("Ожидалась ошибка ValueError")


def test_load_tasks_with_missing_fields(tmp_path, monkeypatch):
    data_file = tmp_path / "tasks.json"
    monkeypatch.setattr(storage, "DATA_FILE", data_file)

    data_file.write_text(
        json.dumps({"tasks": []}),
        encoding="utf-8",
    )

    try:
        storage.load_tasks()
    except ValueError as error:
        assert "Не удалось загрузить данные" in str(error)
    else:
        raise AssertionError("Ожидалась ошибка ValueError")


def test_load_tasks_with_invalid_tasks_type(tmp_path):
    data_file = tmp_path / "tasks.json"
    data_file.write_text(
        json.dumps({"tasks": "не список", "next_task_id": 1}),
        encoding="utf-8",
    )

    storage.DATA_FILE = data_file

    with pytest.raises(ValueError, match="Не удалось загрузить данные"):
        storage.load_tasks()


def test_load_tasks_with_invalid_next_id(tmp_path):
    data_file = tmp_path / "tasks.json"
    data_file.write_text(
        json.dumps({"tasks": [], "next_task_id": 0}),
        encoding="utf-8",
    )

    storage.DATA_FILE = data_file

    with pytest.raises(ValueError, match="Не удалось загрузить данные"):
        storage.load_tasks()


def test_load_tasks_with_read_error():
    class BrokenFile:
        def exists(self):
            return True

        def open(self, *args, **kwargs):
            raise OSError("Нет доступа к файлу")

    storage.DATA_FILE = BrokenFile()

    with pytest.raises(OSError, match="Ошибка чтения файла данных"):
        storage.load_tasks()
