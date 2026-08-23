from __future__ import annotations

from .graph import TopologyGraph, render_mermaid


def render_report(app_name: str, namespace: str, graph: TopologyGraph) -> str:
    lines = [
        f"# {app_name} Application Topology",
        "",
        f"Namespace: `{namespace}`",
        "",
        "## Graph",
        "",
        "```mermaid",
        render_mermaid(graph),
        "```",
        "",
    ]

    for section in sorted(graph.details):
        rows = graph.details[section]
        if not rows:
            continue
        headers = sorted({key for row in rows for key in row})
        lines.extend([f"## {section}", "", _table(headers, rows), ""])

    return "\n".join(lines).rstrip() + "\n"


def _table(headers: list[str], rows: list[dict[str, str]]) -> str:
    output = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        output.append("| " + " | ".join(_cell(row.get(header, "")) for header in headers) + " |")
    return "\n".join(output)


def _cell(value: str) -> str:
    return str(value).replace("|", "\\|")
