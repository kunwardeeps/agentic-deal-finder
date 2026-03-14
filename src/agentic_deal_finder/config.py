from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

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
