from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
TASKS_FILE = DATA_DIR / "tasks.json"
GAMES_FILE = DATA_DIR / "games.json"
SESSIONS_FILE = DATA_DIR / "sessions.json"
RULES_FILE = DATA_DIR / "rules.json"
MONITOR_STATE_FILE = DATA_DIR / "monitor_state.json"
