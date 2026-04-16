# UML Class Diagram (Variant 2)

```mermaid
classDiagram
    class Task {
        +string task_id
        +string name
        +string status
        +float workload_estimation
    }

    class Game {
        +string game_id
        +string name
        +string process_name
    }

    class GameSession {
        +string session_id
        +string game_id
        +string process_name
        +datetime start_time
        +datetime end_time
        +float duration_seconds
    }

    class WorkloadMetrics {
        +float total_workload
        +float completed_workload
        +float completion_rate
    }

    class RuleDecision {
        +datetime decision_time
        +bool allowed
        +string reason
        +object details
    }

    class Storage {
        +read_json(path, default)
        +write_json(path, data)
    }

    class MonitorState {
        +int baseline_total_bytes
    }

    class Variant2Service {
        +list_tasks()
        +add_task()
        +update_task()
        +delete_task()
        +list_games()
        +add_game()
        +delete_game()
        +refresh_monitor_status()
        +playtime_metrics()
        +workload_metrics()
        +rule_decision()
    }

    class Variant2API {
        +GET /tasks
        +POST /tasks
        +PATCH /tasks/{task_id}
        +DELETE /tasks/{task_id}
        +GET /games
        +POST /games
        +DELETE /games/{game_id}
        +GET /monitor/status
        +GET /metrics/playtime
        +GET /metrics/workload
        +GET /rules/decision
    }

    Variant2Service --> Task
    Variant2Service --> Game
    Variant2Service --> GameSession
    Variant2Service --> WorkloadMetrics
    Variant2Service --> RuleDecision
    Variant2Service --> Storage
    Variant2Service --> MonitorState
    Variant2API --> Variant2Service
```
