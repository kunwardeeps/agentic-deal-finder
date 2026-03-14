from __future__ import annotations

from typing import Any, Callable

from agentic_deal_finder.config import load_config
from agentic_deal_finder.models import SearchResult
from agentic_deal_finder.scrapers.duckduckgo_search import search_duckduckgo
from agentic_deal_finder.scrapers.facebook_marketplace import search_facebook_marketplace
from agentic_deal_finder.scrapers.walmart import search_walmart


def _import_langgraph() -> Any:
    try:
        import langgraph

        return langgraph
    except ImportError as exc:
        raise ImportError(
            "langgraph is required to use the LangGraph workflow. "
            "Install it with `pip install langgraph` and try again."
        ) from exc


def create_workflow() -> Any:
    """Create a LangGraph workflow that runs the three agents in parallel."""

    langgraph = _import_langgraph()

    # The exact API may vary between LangGraph versions.
    # This is a best-effort implementation based on typical graph-builder patterns.
    # If the package API differs, this module will raise an ImportError or AttributeError.

    Workflow = getattr(langgraph, "Workflow", None) or getattr(langgraph, "Graph", None)
    if Workflow is None:
        raise RuntimeError("Could not locate Workflow/Graph class in langgraph package")

    wf = Workflow(name="agentic_deal_finder")

    @wf.node(name="standard_search")
    def standard_search(query: str) -> SearchResult:
        deals = search_walmart(query)
        return SearchResult(query=query, deals=deals, source="standard")

    @wf.node(name="used_search")
    def used_search(query: str) -> SearchResult:
        deals = search_facebook_marketplace(query)
        return SearchResult(query=query, deals=deals, source="used")

    @wf.node(name="web_search")
    def web_search(query: str) -> SearchResult:
        config = load_config()
        deals = search_duckduckgo(query, exclude_domains=config.web_search.exclude_domains)
        return SearchResult(query=query, deals=deals, source="web")

    @wf.node(name="generate_report")
    def generate_report(query: str, results: list[SearchResult]) -> str:
        from agentic_deal_finder.report import generate_markdown_report

        out_path = generate_markdown_report(query, results)
        return str(out_path)

    wf.connect(standard_search, generate_report, position=0)
    wf.connect(used_search, generate_report, position=1)
    wf.connect(web_search, generate_report, position=2)

    return wf


def run_workflow(query: str) -> str:
    wf = create_workflow()

    # Execute the workflow. This is an assumption about API.
    if hasattr(wf, "run"):
        return wf.run(query=query)

    if hasattr(wf, "execute"):
        return wf.execute(query=query)

    raise RuntimeError("LangGraph workflow does not expose a run/execute method")
