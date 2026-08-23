from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass(frozen=True)
class AppConfig:
    name: str
    namespace: str
    selector: dict[str, str]


def load_app_config(config_path: str | Path, app_name: str) -> AppConfig:
    data = yaml.safe_load(Path(config_path).read_text(encoding="utf-8"))
    apps = data.get("apps") if isinstance(data, dict) else None
    if not isinstance(apps, list):
        raise ValueError("config must contain an apps list")

    for app in apps:
        if not isinstance(app, dict) or app.get("name") != app_name:
            continue
        namespace = app.get("namespace")
        selector = app.get("selector")
        if not isinstance(namespace, str) or not namespace:
            raise ValueError(f"app {app_name} must define namespace")
        if not isinstance(selector, dict) or not selector:
            raise ValueError(f"app {app_name} must define selector labels")
        if not all(isinstance(key, str) and isinstance(value, str) for key, value in selector.items()):
            raise ValueError(f"app {app_name} selector labels must be strings")
        return AppConfig(name=app_name, namespace=namespace, selector=selector)

    raise ValueError(f"app {app_name} not found in topology config")
