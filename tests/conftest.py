import pytest

import storage


@pytest.fixture(autouse=True)
def isolate_storage(tmp_path, monkeypatch):
    monkeypatch.setattr(storage, "DATA_DIR", tmp_path)
    monkeypatch.setattr(storage, "DATA_FILE", tmp_path / "tasks.json")
    storage.tasks = []
    storage.next_task_id = 1
    yield
    storage.tasks = []
    storage.next_task_id = 1
