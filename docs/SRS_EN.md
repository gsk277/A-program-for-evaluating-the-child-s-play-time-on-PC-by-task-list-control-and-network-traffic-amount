# Software Requirements Specification (SRS)

## 1. Project Information
- Project: Variant 2 - Child Play Time Evaluation Program
- Version: 1.0
- Date: 2026-04-15
- Source lessons:
  - Practical_lesson3_development_v3
  - Practical_lesson4_rest

## 2. Goal
Build a program for evaluating child play time on PC by:
- task list control
- network traffic amount

Required flow from lesson:
- Get task list
- Get game list
- Check game start time
- Calc game duration
- Apply rules

Additional required tasks:
- Calculate workload
- Save task list to file

Implementation form:
- REST service (chosen)

## 3. Scope
### In Scope
- Task management (CRUD + file persistence)
- Game list management
- Process monitoring and game start detection
- Playtime calculation
- Workload calculation
- Rule-based decision
- Incremental network usage tracking from baseline state
- REST API
- API documentation page
- Docker container

### Out of Scope
- Mobile app
- Cloud synchronization
- Multi-user authentication

## 4. Functional Requirements
- FR-01: Get task list
- FR-02: Save task list to file
- FR-03: Get game list
- FR-04: Check game start time
- FR-05: Calculate game duration
- FR-06: Calculate workload
- FR-07: Apply rules
- FR-08: Provide REST service
- FR-09: Provide API documentation (`/docs`)
- FR-10: Provide Dockerized deployment

## 5. Data Model
### Task
- task_id: string
- name: string
- status: todo | done
- workload_estimation: number

### Game
- game_id: string
- name: string
- process_name: string

### GameSession
- session_id: string
- game_id: string
- process_name: string
- start_time: datetime
- end_time: datetime | null
- duration_seconds: number

### RuleDecision
- decision_time: datetime
- allowed: boolean
- reason: string
- details: object
  - includes incremental network usage (from saved baseline)

## 6. API Requirements
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

## 7. Non-Functional Requirements
- NFR-01 Availability: service should run reliably in local environment
- NFR-02 Performance: common API response < 1 second locally
- NFR-03 Maintainability: modular code structure
- NFR-04 Security: no secrets committed to git
- NFR-05 Deployability: Docker build and run should succeed

## 8. Monitoring and Rule Notes
- Monitor status response is focused on tracked games only.
- Network usage in rules is measured as an increment from persisted baseline, not OS lifetime total.

## 9. Acceptance Criteria
- FastAPI service runs successfully
- `/docs` is available
- curl requests succeed for key endpoints
- Variant 2 functional flow is implemented
- Docker image can be built and container can run
- Assignment documents are ready in English

## 9. Clarifications in Current Implementation
- `GET /monitor/status` returns monitored game states only (no full process dump).
- Network condition in rule evaluation uses incremental traffic from baseline, stored in `monitor_state.json`.
