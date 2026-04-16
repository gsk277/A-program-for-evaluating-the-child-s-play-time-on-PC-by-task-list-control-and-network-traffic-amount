from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Task(BaseModel):
    task_id: str
    name: str
    status: str = Field(default="todo", pattern="^(todo|done)$")
    workload_estimation: float = Field(default=1.0, ge=0)


class TaskCreate(BaseModel):
    name: str
    workload_estimation: float = Field(default=1.0, ge=0)


class TaskUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = Field(default=None, pattern="^(todo|done)$")
    workload_estimation: Optional[float] = Field(default=None, ge=0)


class Game(BaseModel):
    game_id: str
    name: str
    process_name: str


class GameCreate(BaseModel):
    name: str
    process_name: str


class GameSession(BaseModel):
    session_id: str
    game_id: str
    process_name: str
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_seconds: float = 0


class WorkloadMetrics(BaseModel):
    total_workload: float
    completed_workload: float
    completion_rate: float


class PlaytimeMetrics(BaseModel):
    total_seconds: float
    by_game: dict[str, float]


class RuleDecision(BaseModel):
    decision_time: datetime
    allowed: bool
    reason: str
    details: dict[str, float]

