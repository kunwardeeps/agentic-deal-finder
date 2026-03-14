from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from agentic_deal_finder.config import load_config
from agentic_deal_finder.langgraph_flow import run_workflow
from agentic_deal_finder.models import SearchResult
from agentic_deal_finder.report import generate_markdown_report
from agentic_deal_finder.scrapers.duckduckgo_search import search_duckduckgo
from agentic_deal_finder.scrapers.facebook_marketplace import search_facebook_marketplace
from agentic_deal_finder.scrapers.walmart import search_walmart


class QueryRequest(BaseModel):
    query: str


app = FastAPI(title="Agentic Deal Finder")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/search/standard")
def search_standard(request: QueryRequest) -> SearchResult:
    deals = search_walmart(request.query)
    return SearchResult(query=request.query, deals=deals, source="standard")


@app.post("/search/used")
def search_used(request: QueryRequest) -> SearchResult:
    deals = search_facebook_marketplace(request.query)
    return SearchResult(query=request.query, deals=deals, source="used")


@app.post("/search/web")
def search_web(request: QueryRequest) -> SearchResult:
    config = load_config()
    deals = search_duckduckgo(request.query, exclude_domains=config.web_search.exclude_domains)
    return SearchResult(query=request.query, deals=deals, source="web")


@app.post("/workflow")
def run_workflow_endpoint(request: QueryRequest) -> dict[str, str]:
    """Run the full agent workflow and generate a Markdown report."""

    # Prefer using LangGraph workflow if available.
    try:
        report_path = run_workflow(request.query)
        return {"report_path": report_path, "workflow": "langgraph"}
    except Exception as exc:
        # Fallback to the direct implementation if LangGraph is missing or fails.
        results = [
            search_standard(request),
            search_used(request),
            search_web(request),
        ]
        out_path = generate_markdown_report(request.query, results)
        return {"report_path": str(out_path), "workflow": "fallback", "error": str(exc)}
