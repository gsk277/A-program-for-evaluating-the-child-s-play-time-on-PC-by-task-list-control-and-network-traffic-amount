import json
from pathlib import Path
from typing import Any


def ensure_file(path: Path, default_value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        write_json(path, default_value)


def read_json(path: Path, default_value: Any) -> Any:
    ensure_file(path, default_value)
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)

