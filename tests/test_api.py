from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.storage import write_json
import app.services as services

client = TestClient(app)


@pytest.fixture(autouse=True)
def isolated_environment(monkeypatch, tmp_path):
    # Use temporary files for every test run to avoid touching real project data.
    tasks_file = tmp_path / "tasks.json"
    games_file = tmp_path / "games.json"
    sessions_file = tmp_path / "sessions.json"
    rules_file = tmp_path / "rules.json"
    monitor_state_file = tmp_path / "monitor_state.json"

    write_json(tasks_file, [])
    write_json(games_file, [])
    write_json(sessions_file, [])
    write_json(
        rules_file,
        {
            "max_play_seconds": 3600,
            "required_completion_rate": 0.5,
            "max_network_mb": 500.0,
        },
    )
    write_json(monitor_state_file, {"baseline_total_bytes": 0})

    monkeypatch.setattr(services, "TASKS_FILE", Path(tasks_file))
    monkeypatch.setattr(services, "GAMES_FILE", Path(games_file))
    monkeypatch.setattr(services, "SESSIONS_FILE", Path(sessions_file))
    monkeypatch.setattr(services, "RULES_FILE", Path(rules_file))
    monkeypatch.setattr(services, "MONITOR_STATE_FILE", Path(monitor_state_file))

    # Mock process list so monitor endpoint is deterministic and fast in CI/local runs.
    class _DummyProcess:
        def __init__(self, name):
            self.info = {"name": name}

    monkeypatch.setattr(
        services.psutil,
        "process_iter",
        lambda attrs=None: [_DummyProcess("python.exe"), _DummyProcess("notepad.exe")],
    )

    # Mock network counters so rule decisions stay deterministic.
    class _DummyNet:
        bytes_sent = 10 * 1024 * 1024
        bytes_recv = 20 * 1024 * 1024

    monkeypatch.setattr(services.psutil, "net_io_counters", lambda: _DummyNet())


def test_ping():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong!"}


def test_task_flow():
    # Create -> update -> read metrics flow for task/workload requirements.
    create = client.post("/tasks", json={"name": "Math homework", "workload_estimation": 2})
    assert create.status_code == 201
    task = create.json()
    task_id = task["task_id"]

    patch = client.patch(f"/tasks/{task_id}", json={"status": "done"})
    assert patch.status_code == 200
    assert patch.json()["status"] == "done"

    metrics = client.get("/metrics/workload")
    assert metrics.status_code == 200
    assert metrics.json()["completion_rate"] >= 0


def test_game_flow():
    # Create game -> refresh monitor -> evaluate rules -> delete game.
    create = client.post("/games", json={"name": "Roblox", "process_name": "robloxplayerbeta.exe"})
    assert create.status_code == 201
    game_id = create.json()["game_id"]

    monitor = client.get("/monitor/status")
    assert monitor.status_code == 200
    payload = monitor.json()
    assert "tracked_games" in payload
    assert "running_processes" not in payload

    decision = client.get("/rules/decision")
    assert decision.status_code == 200
    assert "allowed" in decision.json()

    delete_resp = client.delete(f"/games/{game_id}")
    assert delete_resp.status_code == 204
