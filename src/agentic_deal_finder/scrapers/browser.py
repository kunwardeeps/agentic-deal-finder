from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator


@contextmanager
def playwright_browser_context() -> Iterator[object]:
    """Provide a playwright browser context.

    This helper wraps playwright in a way that allows downstream code to
    use it if available, but fall back gracefully if not.
    """

    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            yield context
            context.close()
            browser.close()
    except Exception:
        # Playwright not installed or cannot launch; yield None to allow fallback.
        yield None


def fetch_html(url: str, timeout: int = 15) -> str:
    """Fetch the rendered HTML of a page using Playwright if possible.

    If Playwright is unavailable, raises an ImportError.
    """

    try:
        from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
    except ImportError as e:
        raise

    with playwright_browser_context() as context:
        if context is None:
            raise ImportError("Playwright is not available; please install it and run `playwright install`.")

        page = context.new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=timeout * 1000)
        # Wait for network to be idle for a short moment; helps JS-heavy pages finish.
        page.wait_for_load_state("networkidle", timeout=timeout * 1000)
        return page.content()
