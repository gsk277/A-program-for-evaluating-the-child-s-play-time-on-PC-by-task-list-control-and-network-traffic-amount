from fastapi import FastAPI, HTTPException

from app.models import GameCreate, TaskCreate, TaskUpdate
from app.services import (
    add_game,
    add_task,
    delete_game,
    delete_task,
    list_games,
    list_tasks,
    playtime_metrics,
    refresh_monitor_status,
    rule_decision,
    update_task,
    workload_metrics,
)

app = FastAPI(
    title="Variant 2 - Child Playtime Control API",
    version="1.0.0",
    description="REST API for task list control, game monitoring, playtime calculation, and rule evaluation.",
)


@app.get("/")
def root():
    return {"message": "Variant 2 API is running"}


@app.get("/ping")
def ping():
    return {"ping": "pong!"}


@app.get("/tasks")
def get_tasks():
    return [t.model_dump() for t in list_tasks()]


@app.post("/tasks", status_code=201)
def create_task(payload: TaskCreate):
    task = add_task(payload.name, payload.workload_estimation)
    return task.model_dump()


@app.patch("/tasks/{task_id}")
def patch_task(task_id: str, payload: TaskUpdate):
    try:
        task = update_task(task_id, payload.model_dump())
        return task.model_dump()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@app.delete("/tasks/{task_id}", status_code=204)
def remove_task(task_id: str):
    try:
        delete_task(task_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@app.get("/games")
def get_games():
    return [g.model_dump() for g in list_games()]


@app.post("/games", status_code=201)
def create_game(payload: GameCreate):
    game = add_game(payload.name, payload.process_name)
    return game.model_dump()


@app.delete("/games/{game_id}", status_code=204)
def remove_game(game_id: str):
    try:
        delete_game(game_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@app.get("/monitor/status")
def monitor_status():
    return refresh_monitor_status()


@app.get("/metrics/playtime")
def metrics_playtime():
    return playtime_metrics()


@app.get("/metrics/workload")
def metrics_workload():
    return workload_metrics().model_dump()


@app.get("/rules/decision")
def rules_decision():
    return rule_decision().model_dump()

