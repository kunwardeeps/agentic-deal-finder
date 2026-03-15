from __future__ import annotations

from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, HttpUrl


class Deal(BaseModel):
    site: str
    title: str
    price: Optional[float]
    currency: Optional[str]
    url: HttpUrl
    condition: Literal["new", "used", "open-box", "unknown"] = "unknown"
    retrieved_at: datetime = datetime.now()


class SearchResult(BaseModel):
    query: str
    deals: list[Deal]
    source: str
    retrieved_at: datetime = datetime.now()
