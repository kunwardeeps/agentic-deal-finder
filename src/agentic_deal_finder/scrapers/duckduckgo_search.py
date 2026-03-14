from __future__ import annotations

from typing import Optional

from duckduckgo_search import DDGS

from agentic_deal_finder.models import Deal
from agentic_deal_finder.scrapers.walmart import _parse_price


def search_duckduckgo(query: str, max_results: int = 10, exclude_domains: list[str] | None = None) -> list[Deal]:
    """Search DuckDuckGo and attempt to scrape a price from the first result page."""

    exclude_domains = exclude_domains or []

    results: list[dict] = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, region="wt-wt", safesearch="Moderate", timelimit=20):
            results.append(r)
            if len(results) >= max_results:
                break

    deals: list[Deal] = []

    for result in results:
        href = result.get("href")
        if not href:
            continue

        # Skip excluded domains
        if any(domain in href for domain in exclude_domains):
            continue

        # Use the snippet to seed the title
        title = result.get("title") or query

        # Attempt to parse a price from the snippet.
        price = _parse_price(result.get("body", ""))

        deals.append(
            Deal(
                site="DuckDuckGo Search",
                title=title,
                price=price,
                currency="USD" if price is not None else None,
                url=href,
                condition="unknown",
            )
        )

        # Only scrape the first non-excluded result to keep it fast.
        break

    return deals
