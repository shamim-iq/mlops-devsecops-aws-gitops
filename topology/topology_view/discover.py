from __future__ import annotations

from collections.abc import Iterable
import json
import subprocess

from .config import AppConfig
from .graph import TopologyGraph


def selector_to_label_selector(selector: dict[str, str]) -> str:
    return ",".join(f"{key}={value}" for key, value in sorted(selector.items()))


def build_static_graph(app: AppConfig) -> TopologyGraph:
    graph = TopologyGraph()
    graph.add_node("app", app.name, "Application")
    graph.add_node("namespace", app.namespace, "Namespace")
    graph.add_node("selector", selector_to_label_selector(app.selector), "Selector")
    graph.add_edge("namespace", "app", "contains")
    graph.add_edge("app", "selector", "selects")
    graph.add_detail("Application", {"name": app.name, "namespace": app.namespace})
    graph.add_detail("Selector", {"labels": selector_to_label_selector(app.selector)})
    return graph


def discover_from_cluster(app: AppConfig) -> TopologyGraph:
    graph = build_static_graph(app)
    label_selector = selector_to_label_selector(app.selector)

    pods = _kubectl_items(app.namespace, "pods", label_selector)
    services = _kubectl_items(app.namespace, "services")
    configmaps = _kubectl_items(app.namespace, "configmaps")
    secrets = _kubectl_items(app.namespace, "secrets")
    pvcs = _kubectl_items(app.namespace, "persistentvolumeclaims")
    deployments = _kubectl_items(app.namespace, "deployments", label_selector)
    replicasets = _kubectl_items(app.namespace, "replicasets", label_selector)
    ingresses = _kubectl_items(app.namespace, "ingresses")
    hpas = _kubectl_items(app.namespace, "horizontalpodautoscalers")
    events = _kubectl_items(app.namespace, "events")
    rollouts = _kubectl_items(app.namespace, "rollouts.argoproj.io")

    _add_named_items(graph, "Deployment", deployments)
    _add_named_items(graph, "ReplicaSet", replicasets)
    _add_named_items(graph, "Pod", pods)
    _add_named_items(graph, "Service", services)
    _add_named_items(graph, "Ingress", ingresses)
    _add_named_items(graph, "ConfigMap", configmaps)
    _add_named_items(graph, "Secret", secrets)
    _add_named_items(graph, "PVC", pvcs)
    _add_named_items(graph, "HPA", hpas)
    _add_rollouts(graph, rollouts)

    for pod in pods:
        pod_id = _node_id("Pod", _metadata(pod)["name"])
        graph.add_edge("selector", pod_id, "matches")
        _add_pod_references(graph, pod)

    _add_service_edges(graph, services, pods)
    _add_ingress_edges(graph, ingresses)
    _add_hpa_edges(graph, hpas)
    _add_events(graph, events)
    return graph


def _add_named_items(graph: TopologyGraph, kind: str, items: Iterable[object]) -> None:
    for item in items:
        name = _metadata(item)["name"]
        graph.add_node(_node_id(kind, name), name, kind)
        graph.add_detail(kind, {"name": name})


def _add_rollouts(graph: TopologyGraph, rollouts: Iterable[dict]) -> None:
    for rollout in rollouts:
        name = _metadata(rollout).get("name", "unknown")
        graph.add_node(_node_id("Rollout", name), name, "Rollout")
        graph.add_detail("Rollout", {"name": name})


def _add_pod_references(graph: TopologyGraph, pod: object) -> None:
    pod_id = _node_id("Pod", _metadata(pod)["name"])
    spec = pod.get("spec", {})
    for volume in spec.get("volumes", []):
        if config_map := volume.get("configMap"):
            graph.add_edge(pod_id, _node_id("ConfigMap", config_map["name"]), "volume")
        if secret := volume.get("secret"):
            graph.add_edge(pod_id, _node_id("Secret", secret["secretName"]), "volume")
        if pvc := volume.get("persistentVolumeClaim"):
            graph.add_edge(pod_id, _node_id("PVC", pvc["claimName"]), "volume")
    for container in spec.get("containers", []):
        for env_from in container.get("envFrom", []):
            if config_map := env_from.get("configMapRef"):
                graph.add_edge(pod_id, _node_id("ConfigMap", config_map["name"]), "envFrom")
            if secret := env_from.get("secretRef"):
                graph.add_edge(pod_id, _node_id("Secret", secret["name"]), "envFrom")
        for env in container.get("env", []):
            value_from = env.get("valueFrom")
            if not isinstance(value_from, dict):
                continue
            if config_map := value_from.get("configMapKeyRef"):
                graph.add_edge(pod_id, _node_id("ConfigMap", config_map["name"]), "env")
            if secret := value_from.get("secretKeyRef"):
                graph.add_edge(pod_id, _node_id("Secret", secret["name"]), "env")


def _add_service_edges(graph: TopologyGraph, services: Iterable[object], pods: Iterable[object]) -> None:
    for service in services:
        selector = service.get("spec", {}).get("selector", {})
        if not selector:
            continue
        service_id = _node_id("Service", _metadata(service)["name"])
        for pod in pods:
            labels = _metadata(pod).get("labels", {})
            if all(labels.get(key) == value for key, value in selector.items()):
                graph.add_edge(service_id, _node_id("Pod", _metadata(pod)["name"]), "selects")


def _add_ingress_edges(graph: TopologyGraph, ingresses: Iterable[object]) -> None:
    for ingress in ingresses:
        ingress_id = _node_id("Ingress", _metadata(ingress)["name"])
        for rule in ingress.get("spec", {}).get("rules", []):
            http = rule.get("http")
            if not http:
                continue
            for path in http.get("paths", []):
                service = path.get("backend", {}).get("service")
                if service:
                    graph.add_edge(ingress_id, _node_id("Service", service["name"]), "routes")


def _add_hpa_edges(graph: TopologyGraph, hpas: Iterable[object]) -> None:
    for hpa in hpas:
        target = hpa.get("spec", {}).get("scaleTargetRef", {})
        graph.add_edge(
            _node_id("HPA", _metadata(hpa)["name"]),
            _node_id(target.get("kind", ""), target.get("name", "")),
            "scales",
        )


def _add_events(graph: TopologyGraph, events: Iterable[object]) -> None:
    for event in events:
        involved = event.get("involvedObject", {})
        graph.add_detail(
            "Event",
            {
                "object": f"{involved.get('kind', '')}/{involved.get('name', '')}",
                "reason": event.get("reason", ""),
                "message": event.get("message", ""),
            },
        )


def _kubectl_items(namespace: str, resource: str, label_selector: str | None = None) -> list[dict]:
    command = ["kubectl", "get", resource, "-n", namespace, "-o", "json"]
    if label_selector:
        command.extend(["-l", label_selector])
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    return json.loads(result.stdout).get("items", [])


def _metadata(item: dict) -> dict:
    return item.get("metadata", {})


def _node_id(kind: str, name: str) -> str:
    return f"{kind}:{name}"
