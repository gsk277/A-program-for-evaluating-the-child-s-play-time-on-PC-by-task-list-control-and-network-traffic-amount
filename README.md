# Variant 2 Assignment - Child Playtime Control (REST + FastAPI)-Gao Shuke

This project implements **Variant 2** from the practical lessons:
- Get task list
- Get game list
- Check game start time
- Calculate game duration
- Apply rules
- Calculate workload
- Save task list to file

It is implemented as a **REST service** (FastAPI), with Docker support and test coverage.

## 1. Tech Stack
- Python 3.11+
- FastAPI
- Uvicorn
- psutil
- pytest

## 2. Project Structure
```text
app/
  main.py
  models.py
  services.py
  storage.py
  config.py
data/
  tasks.json
  games.json
  sessions.json
  rules.json
  monitor_state.json
  monitor_state.json
  monitor_state.json
tests/
  test_api.py
docs/
  SRS_EN.md
  Backlog_EN.md
  UML_Class_Diagram.md
  UI_Prototype_EN.md
```

## 3. Local Run
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API base URL:
- `http://127.0.0.1:8000`

Swagger docs:
- `http://127.0.0.1:8000/docs`

## 4. API Endpoints
- `GET /tasks`
- `POST /tasks`
- `PATCH /tasks/{task_id}`
- `DELETE /tasks/{task_id}`
- `GET /games`
- `POST /games`
- `DELETE /games/{game_id}`
- `GET /monitor/status`
- `GET /metrics/playtime`
- `GET /metrics/workload`
- `GET /rules/decision`

Notes:
- `/monitor/status` now returns only tracked game statuses (compact response).
- Network usage in rule decision is calculated as **incremental usage from baseline**, not host lifetime total.

Implementation notes:
- `/monitor/status` returns only tracked game statuses (compact response).
- Network usage in `/rules/decision` is calculated as incremental usage from a stored baseline (`data/monitor_state.json`), not host lifetime total.

## 5. curl Examples
```bash
curl http://127.0.0.1:8000/ping
curl http://127.0.0.1:8000/tasks
curl -X POST http://127.0.0.1:8000/tasks -H "Content-Type: application/json" -d "{\"name\":\"Math homework\",\"workload_estimation\":2}"
curl http://127.0.0.1:8000/metrics/workload
curl http://127.0.0.1:8000/rules/decision
```

Notes:
- `/monitor/status` now returns only tracked-game status to keep payload concise.
- Rule evaluation uses incremental network usage from a stored baseline (`data/monitor_state.json`), not host lifetime counters.

## 6. Docker
Build image:
```bash
docker build -t variant2-playtime-api .
```

Run container:
```bash
docker run -p 8000:8000 variant2-playtime-api
```

## 7. Tests
```bash
pytest -q
```

## 8. Assignment Deliverables (English)
All required documents are in `docs/`:
- SRS
- Backlog with time estimations
- UML class diagram
- UI prototype
