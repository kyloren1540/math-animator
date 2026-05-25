"""Independent variable names for formulas and axis labels."""

from __future__ import annotations

import re

# Presets shown in the UI (display, stored value)
INDEPENDENT_VAR_PRESETS: list[tuple[str, str]] = [
    ("x", "x"),
    ("t (tiempo)", "t"),
    ("u", "u"),
    ("s", "s"),
    ("n", "n"),
    ("θ (theta)", "θ"),
    ("Otra…", "__custom__"),
]

_LATEX_MAP = {
    "θ": r"\theta",
    "alpha": r"\alpha",
    "beta": r"\beta",
    "gamma": r"\gamma",
    "omega": r"\omega",
    "phi": r"\phi",
    "lambda": r"\lambda",
}


def normalize_independent_var(name: str) -> str:
    """Single-letter or short identifier for formulas."""
    v = (name or "x").strip()
    if not v:
        return "x"
    if len(v) > 8:
        v = v[:8]
    if not re.match(r"^[\w\u03B1-\u03C9]+$", v, re.UNICODE):
        return "x"
    return v


def independent_var_to_latex(var: str) -> str:
    v = normalize_independent_var(var)
    return _LATEX_MAP.get(v, v)
