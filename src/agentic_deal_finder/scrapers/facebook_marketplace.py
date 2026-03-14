from __future__ import annotations

import re
from typing import Optional

import requests
from bs4 import BeautifulSoup

from agentic_deal_finder.models import Deal
from agentic_deal_finder.scrapers.browser import fetch_html


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    " AppleWebKit/537.36 (KHTML, like Gecko)"
    " Chrome/125.0.0.0 Safari/537.36",
}


def _parse_price(text: str) -> Optional[float]:
    if not text:
        return None
    match = re.search(r"\$?\s*([0-9,]+(?:\.[0-9]{1,2})?)", text)
    if not match:
        return None
    try:
        return float(match.group(1).replace(",", ""))
    except ValueError:
        return None


def search_facebook_marketplace(query: str, max_results: int = 1) -> list[Deal]:
    """Search Facebook Marketplace for a product and return the first matching price.

    Note: Facebook Marketplace is heavily JS-driven and may block requests.
    """

    url = f"https://www.facebook.com/marketplace/search/?query={requests.utils.quote(query)}"

    try:
        html = fetch_html(url)
    except Exception:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        html = resp.text

    soup = BeautifulSoup(html, "html.parser")

    # Find listing cards - Marketplace markup changes often.
    card = soup.select_one("[role='article']") or soup.select_one("[data-testid='marketplace_feed_item']")
    if not card:
        return []

    title_el = card.select_one("h3")
    title = title_el.get_text(strip=True) if title_el else query

    link_el = card.select_one("a")
    href = link_el["href"] if link_el and link_el.has_attr("href") else url

    price_el = card.select_one("div[aria-label*='Price']")
    if not price_el:
        # fallback to any text that looks like a price
        price_el = card.find(text=re.compile(r"\$[0-9]"))
        price_text = price_el.strip() if isinstance(price_el, str) else ""
    else:
        price_text = price_el.get_text(" ", strip=True)

    price = _parse_price(price_text)

    return [
        Deal(
            site="Facebook Marketplace",
            title=title,
            price=price,
            currency="USD" if price is not None else None,
            url=href,
            condition="used",
        )
    ]
