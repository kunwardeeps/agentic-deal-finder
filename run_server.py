"""Run the Agentic Deal Finder FastAPI server.

This script ensures the `src/` layout is importable by adding it to sys.path
before importing and running the application.

Usage:
    python run_server.py

You can also pass any args accepted by the package CLI, e.g.:
    python run_server.py --host 0.0.0.0 --port 8005
"""

from __future__ import annotations

import os
import sys

# Ensure we can import the package from the src/ layout.
ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from agentic_deal_finder.__main__ import main

if __name__ == "__main__":
    # Forward CLI args to the package entrypoint.
    main(argv=sys.argv[1:])
