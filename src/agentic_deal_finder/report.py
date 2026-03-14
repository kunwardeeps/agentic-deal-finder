from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Iterable

from agentic_deal_finder.models import Deal, SearchResult


def format_deal(deal: Deal) -> str:
    parts: list[str] = []
    parts.append(f"- **{deal.title}**")
    if deal.price is not None:
        parts.append(f"${deal.price:,.2f}")
    if deal.currency:
        parts.append(deal.currency)
    if deal.condition and deal.condition != "unknown":
        parts.append(f"({deal.condition})")
    parts.append(f"[{deal.site}]({deal.url})")
    return " ".join(parts)


def generate_markdown_report(query: str, results: Iterable[SearchResult], output_dir: Path | None = None) -> Path:
    now = datetime.utcnow()
    output_dir = Path(output_dir or Path("reports")).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    filename = f"deal-report-{query.replace(' ', '_')}-{now.strftime('%Y%m%dT%H%M%SZ')}.md"
    out_path = output_dir / filename

    lines: list[str] = []
    lines.append(f"# Deal Finder Report")
    lines.append("")
    lines.append(f"**Query:** {query}")
    lines.append(f"**Generated:** {now.isoformat()}Z")
    lines.append("")

    for result in results:
        lines.append(f"## Results from {result.source}")
        lines.append("")
        if not result.deals:
            lines.append("No results found.")
            lines.append("")
            continue
        for deal in result.deals:
            lines.append(format_deal(deal))
        lines.append("")

    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path
