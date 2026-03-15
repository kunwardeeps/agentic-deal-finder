from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List
import logging
from logging.handlers import RotatingFileHandler

import yaml


@dataclass(frozen=True)
class SiteEntry:
    name: str
    url_template: str


@dataclass(frozen=True)
class WebSearchConfig:
    exclude_domains: List[str]


@dataclass(frozen=True)
class Config:
    standard_sites: List[SiteEntry]
    used_sites: List[SiteEntry]
    web_search: WebSearchConfig


def load_config(path: str | Path | None = None) -> Config:
    path = Path(path or Path(__file__).resolve().parents[1] / "config" / "sites.yaml")

    with open(path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}

    def _load_sites(key: str) -> List[SiteEntry]:
        items = raw.get(key, []) or []
        return [SiteEntry(name=i["name"], url_template=i["url_template"]) for i in items]

    web_search_raw: Dict[str, Any] = raw.get("web_search", {}) or {}

    return Config(
        standard_sites=_load_sites("standard"),
        used_sites=_load_sites("used"),
        web_search=WebSearchConfig(exclude_domains=web_search_raw.get("exclude_domains", []) or []),
    )


def setup_logging(log_level: str = "INFO", log_file: str | Path | None = None) -> None:
    """Set up application logging to console and file.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file. If None, uses 'logs/app.log' relative to project root.
    """
    if log_file is None:
        # Default to logs/app.log in project root
        project_root = Path(__file__).resolve().parents[1]
        log_file = project_root / "logs" / "app.log"

    log_file = Path(log_file)
    log_file.parent.mkdir(parents=True, exist_ok=True)

    # Create logger
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    # Remove existing handlers to avoid duplicates
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler with rotation (10MB max, keep 5 backups)
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Log the setup
    logger.info(f"Logging configured. Level: {log_level}, File: {log_file}")
