from __future__ import annotations

import re
from typing import Optional

import requests
from bs4 import BeautifulSoup

from agentic_deal_finder.models import Deal
from agentic_deal_finder.scrapers.browser import fetch_html

import logging

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
}

logger = logging.getLogger(__name__)

def _parse_price(text: str) -> Optional[float]:
    if not text:
        return None
    # Common price formats like "$1,234.56" or "1,234.56"
    match = re.search(r"\$?\s*([0-9,]+(?:\.[0-9]{1,2})?)", text)
    if not match:
        return None
    value = match.group(1).replace(",", "")
    try:
        return float(value)
    except ValueError:
        return None


def search_walmart(query: str, max_results: int = 1) -> list[Deal]:
    """Search Walmart for a product and return the first matching price.

    This implementation uses Playwright (when available) to load Walmart’s
    JavaScript-driven search results.
    """
    logger.info(f"Searching Walmart for query: {query}")

    url = f"https://www.walmart.com/search?q={requests.utils.quote(query)}"

    try:
        html = fetch_html(url)
        logger.info(f"Fetched HTML for Walmart search: {url}")
    except Exception as e:
        logger.warning(f"Playwright fetch failed for Walmart, falling back to requests: {e}")
        # Fall back to non-JS fetch if Playwright is unavailable.
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        html = resp.text
        logger.info(f"Fetched HTML via requests for Walmart search: {url}")

    soup = BeautifulSoup(html, "html.parser")

    # Walmart uses structured data; try to find the first product card.
    card = soup.select_one("[data-tl-id='ProductTileGridView']")
    if not card:
        card = soup.select_one("[data-item-id]")

    if not card:
        logger.warning(f"No product card found for Walmart search: {query}")
        return []

    title_el = card.select_one(".product-title-link span")
    title = title_el.get_text(strip=True) if title_el else ""
    logger.debug(f"Extracted title: {title}")

    link_el = card.select_one("a.product-title-link")
    href = link_el["href"] if link_el and link_el.has_attr("href") else None
    if href and href.startswith("/"):
        href = f"https://www.walmart.com{href}"
    logger.debug(f"Extracted href: {href}")

    price_el = card.select_one("span.visuallyhidden")
    price_text = price_el.get_text(" ", strip=True) if price_el else ""
    price = _parse_price(price_text)
    logger.debug(f"Extracted price text: '{price_text}', parsed price: {price}")

    result = [
        Deal(
            site="Walmart",
            title=title or query,
            price=price,
            currency="USD" if price is not None else None,
            url=href or url,
            condition="new",
        )
    ]
    logger.info(f"Walmart search completed for '{query}', found {len(result)} results")
    return result
