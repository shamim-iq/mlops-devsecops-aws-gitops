from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class TopologyNode:
    id: str
    label: str
    kind: str


@dataclass(frozen=True)
class TopologyEdge:
    source: str
    target: str
    label: str


@dataclass
class TopologyGraph:
    nodes: dict[str, TopologyNode] = field(default_factory=dict)
    edges: list[TopologyEdge] = field(default_factory=list)
    details: dict[str, list[dict[str, str]]] = field(default_factory=dict)

    def add_node(self, node_id: str, label: str, kind: str) -> None:
        self.nodes[node_id] = TopologyNode(id=node_id, label=label, kind=kind)

    def add_edge(self, source: str, target: str, label: str) -> None:
        if source in self.nodes and target in self.nodes:
            self.edges.append(TopologyEdge(source=source, target=target, label=label))

    def add_detail(self, section: str, row: dict[str, str]) -> None:
        self.details.setdefault(section, []).append(row)


def mermaid_id(value: str) -> str:
    cleaned = "".join(char if char.isalnum() else "_" for char in value)
    if cleaned and cleaned[0].isdigit():
        return f"n_{cleaned}"
    return cleaned or "node"


def render_mermaid(graph: TopologyGraph) -> str:
    lines = ["flowchart LR"]
    id_map = {node_id: mermaid_id(node_id) for node_id in graph.nodes}

    for node in sorted(graph.nodes.values(), key=lambda item: item.id):
        lines.append(f'  {id_map[node.id]}["{node.kind}: {node.label}"]')

    for edge in graph.edges:
        lines.append(f'  {id_map[edge.source]} -->|"{edge.label}"| {id_map[edge.target]}')

    return "\n".join(lines)
