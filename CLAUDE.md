# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Development Tasks

### Setup
```bash
# Install dependencies
python -m pip install -r requirements.txt
# Install Playwright browsers
python -m playwright install
```

### Running the Server
```bash
# Run the FastAPI server on default host and port (127.0.0.1:8000)
python -m agentic_deal_finder --run

# Specify custom host and port
python -m agentic_deal_finder --host 0.0.0.0 --port 8080 --run
```

### Testing
```bash
# Run all tests
python -m pytest

# Run a specific test (e.g., health check)
python -m pytest src/agentic_deal_finder/tests/test_integration.py::TestDealFinderIntegration::test_health_check
```

### Making API Requests
```bash
# Example: Search for Nintendo Switch deals
curl -X POST "http://127.0.0.1:8000/workflow" -H "Content-Type: application/json" -d '{"query": "Nintendo Switch"}'
```

## Project Architecture

### High-Level Structure
- **Entry Point**: `src/agentic_deal_finder/__main__.py` - Parses command-line arguments and starts the FastAPI server.
- **Web Server**: `src/agentic_deal_finder/server.py` - Defines FastAPI endpoints, including the `/workflow` endpoint that triggers the deal-finding process.
- **Workflow Orchestration**: `src/agentic_deal_finder/langgraph_flow.py` - Uses LangGraph to define the agent workflow for searching deals across multiple sources.
- **Scrapers**: Located in `src/agentic_deal_finder/scrapers/` - Individual scraper implementations for different sites (e.g., Facebook Marketplace, DuckDuckGo, Walmart).
- **Configuration**: `config/sites.yaml` - YAML file defining site lists for standard, used, and web search (with exclusions).
- **Reporting**: `src/agentic_deal_finder/report.py` - Generates Markdown reports from the search results.
- **Data Models**: `src/agentic_deal_finder/models.py` - Pydantic models for deal data and workflow state.
- **Configuration & Logging**: `src/agentic_deal_finder/config.py` - Handles loading configuration from YAML and setting up logging.

### Key Components
1. **Workflow Endpoint** (`server.py`): Accepts a POST request with a search query, triggers the LangGraph workflow, and returns a report path.
2. **LangGraph Flow** (`langgraph_flow.py`): Orchestrates the scraping process across standard sites, used sites, and web search, then compiles results.
3. **Scrapers**: Each scraper implements site-specific logic to extract deal information (title, price, URL, etc.).
4. **Report Generation**: Formats collected deals into a Markdown report saved in the `reports/` directory.

### Configuration
- Site configurations are defined in `config/sites.yaml` with three categories:
  - `standard`: New product listings (e.g., retail sites)
  - `used`: Used/open-box listings (e.g., Facebook Marketplace)
  - `web_search`: General web search with domain exclusions
- Logging is configured to output to both console and a rotating file (`logs/app.log`).

### Data Flow
1. User sends query to `/workflow` endpoint.
2. Workflow orchestrator (`langgraph_flow.py`) processes the query:
   - Searches standard sites using their scrapers.
   - Searches used sites using their scrapers.
   - Performs web search (DuckDuckGo) excluding specified domains.
3. Results are aggregated and passed to the report generator.
4. A Markdown report is saved and the report path is returned to the user.
