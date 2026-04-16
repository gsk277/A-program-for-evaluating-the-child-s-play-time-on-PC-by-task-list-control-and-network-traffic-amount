# UI Prototype (Variant 2)

## 1. Purpose
This prototype defines a simple web dashboard for parents to:
- manage tasks
- manage game list
- monitor playtime
- review rule decision

## 2. Screen List
1. Dashboard
2. Task Management
3. Game Management
4. Monitoring & Metrics
5. Rule Decision

## 3. Wireframe Description

### 3.1 Dashboard
- Header: `Variant 2 Playtime Control`
- KPI cards:
  - Total Workload
  - Completion Rate
  - Total Playtime
  - Rule Decision (`Allowed` / `Denied`)
- Quick buttons:
  - Add Task
  - Add Game
  - Refresh Monitor

### 3.2 Task Management
- Table columns:
  - Task ID
  - Name
  - Status
  - Workload
  - Actions (`Edit`, `Done`, `Delete`)
- Form:
  - Task Name input
  - Workload input
  - Submit button

### 3.3 Game Management
- Table columns:
  - Game ID
  - Name
  - Process Name
  - Actions (`Delete`)
- Form:
  - Game Name input
  - Process Name input
  - Submit button

### 3.4 Monitoring & Metrics
- Running process list panel
- Session timeline panel
- Playtime by game panel
- Refresh button

### 3.5 Rule Decision
- Status badge: `Allowed` or `Denied`
- Reason text block
- Details:
  - completion rate
  - total playtime seconds
  - network usage MB
  - thresholds

## 4. API Mapping
- Task page -> `/tasks`
- Game page -> `/games`
- Monitoring page -> `/monitor/status`, `/metrics/playtime`, `/metrics/workload`
- Rule page -> `/rules/decision`

## 5. Prototype Conclusion
This UI prototype is intentionally minimal and aligned with Variant 2 required workflow from the practical lesson.

