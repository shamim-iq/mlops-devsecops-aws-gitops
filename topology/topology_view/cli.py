from __future__ import annotations

import argparse
from pathlib import Path

from .config import load_app_config
from .discover import discover_from_cluster
from .render_markdown import render_report


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a Kubernetes application topology report.")
    parser.add_argument("--config", required=True, help="Path to topology apps YAML.")
    parser.add_argument("--app", required=True, help="Application name from the config file.")
    parser.add_argument("--output", required=True, help="Markdown report output path.")
    args = parser.parse_args()

    app = load_app_config(args.config, args.app)
    graph = discover_from_cluster(app)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_report(app.name, app.namespace, graph), encoding="utf-8")


if __name__ == "__main__":
    main()
