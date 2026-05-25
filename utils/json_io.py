"""Import/export functions as JSON."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from functions.base import MathFunction
from functions.factory import create_function


def export_functions(functions: list[MathFunction], path: str | Path) -> None:
    data = {
        "version": 1,
        "functions": [f.to_dict() for f in functions],
    }
    Path(path).write_text(
        json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def import_functions(path: str | Path) -> list[MathFunction]:
    raw: dict[str, Any] = json.loads(Path(path).read_text(encoding="utf-8"))
    result: list[MathFunction] = []
    for item in raw.get("functions", []):
        fn = create_function(
            item["type_id"],
            item.get("params"),
            item.get("color"),
            item.get("independent_var"),
        )
        fn.meta.visible = item.get("visible", True)
        result.append(fn)
    return result
