from __future__ import annotations

import argparse

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from agentic_deal_finder.server import app


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="agentic-deal-finder")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind the server to")
    parser.add_argument("--port", type=int, default=8000, help="Port to run the server on")
    parser.add_argument("--run", action="store_true", help="Run the FastAPI server")
    args = parser.parse_args(argv)

    if args.run:
        # Allow CORS for local testing.
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        uvicorn.run(app, host=args.host, port=args.port)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
