#!/usr/bin/env python3
"""Math Animator — Educational function visualizer."""

import sys
from pathlib import Path

# Ensure project root is on sys.path
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ui.main_window import run_app


def main() -> None:
    raise SystemExit(run_app())


if __name__ == "__main__":
    main()
