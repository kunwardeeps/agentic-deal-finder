# agentic-deal-finder

Agentic Deal Finder uses multiple specialized agents to search for deals across ecommerce websites, including standard new product listings, used/open-box listings, and web search results.

## Run (Development)

1. Install dependencies:

```bash
python -m pip install -r requirements.txt
python -m playwright install
```

2. Run the FastAPI server:

```bash
python -m agentic_deal_finder --run
```

3. Call the workflow endpoint:

```bash
curl -X POST "http://127.0.0.1:8000/workflow" -H "Content-Type: application/json" -d '{"query": "Nintendo Switch"}'
```

The endpoint returns a JSON response with `report_path` pointing to the generated Markdown report.

## Project Structure

- `src/agentic_deal_finder/scrapers/` — individual site scraper implementations.
- `config/sites.yaml` — configurable site lists (standard, used, web search exclusions).
- `reports/` — generated Markdown reports.
- `src/agentic_deal_finder/server.py` — FastAPI endpoints (acting as the MCP server).
