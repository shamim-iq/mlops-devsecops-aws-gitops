import pytest

from topology.topology_view.config import AppConfig, load_app_config
from topology.topology_view.discover import build_static_graph, selector_to_label_selector
from topology.topology_view.graph import TopologyGraph, render_mermaid
from topology.topology_view.render_markdown import render_report


def test_load_app_config_reads_selected_app() -> None:
    app = load_app_config("tests/fixtures/topology/apps.yaml", "prediction-api")

    assert app == AppConfig(
        name="prediction-api",
        namespace="prediction-api",
        selector={"app.kubernetes.io/name": "prediction-api"},
    )


def test_load_app_config_rejects_missing_app() -> None:
    with pytest.raises(ValueError, match="not found"):
        load_app_config("tests/fixtures/topology/empty-apps.yaml", "prediction-api")


def test_selector_to_label_selector_is_stable() -> None:
    selector = {"tier": "api", "app.kubernetes.io/name": "prediction-api"}

    assert selector_to_label_selector(selector) == "app.kubernetes.io/name=prediction-api,tier=api"


def test_render_mermaid_includes_nodes_and_edges() -> None:
    graph = TopologyGraph()
    graph.add_node("Service:prediction-api", "prediction-api", "Service")
    graph.add_node("Pod:prediction-api-abc", "prediction-api-abc", "Pod")
    graph.add_edge("Service:prediction-api", "Pod:prediction-api-abc", "selects")

    output = render_mermaid(graph)

    assert "flowchart LR" in output
    assert 'Service_prediction_api["Service: prediction-api"]' in output
    assert 'Service_prediction_api -->|"selects"| Pod_prediction_api_abc' in output


def test_render_report_includes_graph_and_detail_tables() -> None:
    app = AppConfig(
        name="prediction-api",
        namespace="prediction-api",
        selector={"app.kubernetes.io/name": "prediction-api"},
    )
    graph = build_static_graph(app)

    report = render_report(app.name, app.namespace, graph)

    assert "# prediction-api Application Topology" in report
    assert "```mermaid" in report
    assert "## Application" in report
    assert "| name | namespace |" in report
