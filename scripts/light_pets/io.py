"""JSON 与路径工具。"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .config import ROOT


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def demo_rel(path: Path) -> str:
    return "../" + rel(path)
