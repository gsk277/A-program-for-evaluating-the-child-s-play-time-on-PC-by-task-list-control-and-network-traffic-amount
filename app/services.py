from datetime import datetime
from uuid import uuid4

import psutil

from app.config import GAMES_FILE, MONITOR_STATE_FILE, RULES_FILE, SESSIONS_FILE, TASKS_FILE
from app.models import Game, GameSession, RuleDecision, Task, WorkloadMetrics
from app.storage import read_json, write_json


DEFAULT_RULES = {
    "max_play_seconds": 3600,
    "required_completion_rate": 0.5,
    "max_network_mb": 500.0,
}


def list_tasks() -> list[Task]:
    raw = read_json(TASKS_FILE, [])
    return [Task(**item) for item in raw]


def add_task(name: str, workload_estimation: float) -> Task:
    tasks = list_tasks()
    task = Task(
        task_id=str(uuid4()),
        name=name,
        status="todo",
        workload_estimation=workload_estimation,
    )
    tasks.append(task)
    write_json(TASKS_FILE, [t.model_dump() for t in tasks])
    return task


def update_task(task_id: str, payload: dict) -> Task:
    tasks = list_tasks()
    updated = None
    for idx, task in enumerate(tasks):
        if task.task_id == task_id:
            task_data = task.model_dump()
            for k, v in payload.items():
                if v is not None:
                    task_data[k] = v
            updated = Task(**task_data)
            tasks[idx] = updated
            break
    if updated is None:
        raise ValueError("Task not found")
    write_json(TASKS_FILE, [t.model_dump() for t in tasks])
    return updated


def delete_task(task_id: str) -> None:
    tasks = list_tasks()
    filtered = [t for t in tasks if t.task_id != task_id]
    if len(filtered) == len(tasks):
        raise ValueError("Task not found")
    write_json(TASKS_FILE, [t.model_dump() for t in filtered])


def list_games() -> list[Game]:
    raw = read_json(GAMES_FILE, [])
    return [Game(**item) for item in raw]


def add_game(name: str, process_name: str) -> Game:
    games = list_games()
    game = Game(game_id=str(uuid4()), name=name, process_name=process_name)
    games.append(game)
    write_json(GAMES_FILE, [g.model_dump() for g in games])
    return game


def delete_game(game_id: str) -> None:
    games = list_games()
    filtered = [g for g in games if g.game_id != game_id]
    if len(filtered) == len(games):
        raise ValueError("Game not found")
    write_json(GAMES_FILE, [g.model_dump() for g in filtered])


def _read_sessions() -> list[GameSession]:
    # Sessions are stored in JSON, so timestamps need explicit conversion back to datetime.
    raw = read_json(SESSIONS_FILE, [])
    sessions = []
    for item in raw:
        item["start_time"] = datetime.fromisoformat(item["start_time"])
        if item.get("end_time"):
            item["end_time"] = datetime.fromisoformat(item["end_time"])
        sessions.append(GameSession(**item))
    return sessions


def _write_sessions(sessions: list[GameSession]) -> None:
    # Convert datetime fields into ISO strings for JSON persistence.
    payload = []
    for s in sessions:
        dumped = s.model_dump()
        dumped["start_time"] = s.start_time.isoformat()
        dumped["end_time"] = s.end_time.isoformat() if s.end_time else None
        payload.append(dumped)
    write_json(SESSIONS_FILE, payload)


def refresh_monitor_status() -> dict:
    # Read tracked games and currently running processes, then synchronize session states.
    games = list_games()
    running_processes = {p.info.get("name", "").lower() for p in psutil.process_iter(["name"])}
    sessions = _read_sessions()

    now = datetime.utcnow()
    # "Active" means a session with no end_time yet.
    active_session_game_ids = {s.game_id for s in sessions if s.end_time is None}

    started = []
    stopped = []

    for game in games:
        is_running = game.process_name.lower() in running_processes
        has_active = game.game_id in active_session_game_ids

        if is_running and not has_active:
            # Game has just started: create a new active session.
            session = GameSession(
                session_id=str(uuid4()),
                game_id=game.game_id,
                process_name=game.process_name,
                start_time=now,
            )
            sessions.append(session)
            started.append(game.process_name)

        if (not is_running) and has_active:
            # Game has stopped: close the active session and store duration.
            for session in sessions:
                if session.game_id == game.game_id and session.end_time is None:
                    session.end_time = now
                    session.duration_seconds = (session.end_time - session.start_time).total_seconds()
                    stopped.append(game.process_name)

    _write_sessions(sessions)
    # Return only tracked game statuses to keep response compact and assignment-focused.
    active_session_ids = {s.game_id for s in sessions if s.end_time is None}
    game_statuses = []
    for game in games:
        game_statuses.append(
            {
                "game_id": game.game_id,
                "name": game.name,
                "process_name": game.process_name,
                "is_running": game.process_name.lower() in running_processes,
                "has_active_session": game.game_id in active_session_ids,
            }
        )

    return {"started": started, "stopped": stopped, "tracked_games": game_statuses}


def playtime_metrics() -> dict:
    sessions = _read_sessions()
    now = datetime.utcnow()

    by_game: dict[str, float] = {}
    total = 0.0

    for session in sessions:
        duration = session.duration_seconds
        if session.end_time is None:
            # For active sessions, calculate up-to-now duration on the fly.
            duration = (now - session.start_time).total_seconds()
        total += duration
        by_game[session.process_name] = by_game.get(session.process_name, 0.0) + duration

    return {"total_seconds": total, "by_game": by_game}


def workload_metrics() -> WorkloadMetrics:
    tasks = list_tasks()
    total_workload = sum(t.workload_estimation for t in tasks)
    completed_workload = sum(t.workload_estimation for t in tasks if t.status == "done")
    completion_rate = (completed_workload / total_workload) if total_workload > 0 else 0.0
    return WorkloadMetrics(
        total_workload=total_workload,
        completed_workload=completed_workload,
        completion_rate=completion_rate,
    )


def get_rules() -> dict:
    rules = read_json(RULES_FILE, DEFAULT_RULES)
    for k, v in DEFAULT_RULES.items():
        # Ensure missing keys are auto-filled to keep backward compatibility.
        if k not in rules:
            rules[k] = v
    write_json(RULES_FILE, rules)
    return rules


def network_usage_mb() -> float:
    # Compute session/network usage increment from baseline to avoid using host lifetime total.
    io = psutil.net_io_counters()
    current_total_bytes = io.bytes_sent + io.bytes_recv
    state = read_json(MONITOR_STATE_FILE, {"baseline_total_bytes": current_total_bytes})

    baseline = int(state.get("baseline_total_bytes", current_total_bytes))
    if current_total_bytes < baseline:
        # Handle counter reset or overflow by re-baselining.
        baseline = current_total_bytes

    increment_bytes = current_total_bytes - baseline
    write_json(MONITOR_STATE_FILE, {"baseline_total_bytes": baseline})
    return increment_bytes / (1024 * 1024)


def rule_decision() -> RuleDecision:
    # Rule evaluation combines workload completion, playtime, and network traffic.
    wl = workload_metrics()
    pt = playtime_metrics()
    rules = get_rules()
    network_mb = network_usage_mb()

    allowed = True
    reasons = []

    if wl.completion_rate < float(rules["required_completion_rate"]):
        allowed = False
        reasons.append("Completion rate below required threshold")
    if pt["total_seconds"] > float(rules["max_play_seconds"]):
        allowed = False
        reasons.append("Playtime exceeded max limit")
    if network_mb > float(rules["max_network_mb"]):
        allowed = False
        reasons.append("Network usage exceeded max limit")

    reason = "Allowed to play" if allowed else "; ".join(reasons)
    return RuleDecision(
        decision_time=datetime.utcnow(),
        allowed=allowed,
        reason=reason,
        details={
            "completion_rate": wl.completion_rate,
            "total_playtime_seconds": pt["total_seconds"],
            "network_usage_mb": network_mb,
            "required_completion_rate": float(rules["required_completion_rate"]),
            "max_play_seconds": float(rules["max_play_seconds"]),
            "max_network_mb": float(rules["max_network_mb"]),
        },
    )
