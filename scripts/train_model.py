from __future__ import annotations

import pickle
from pathlib import Path

from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


MODEL_VERSION = "iris-logreg-0.1.0"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = PROJECT_ROOT / "app" / "model" / "model.pkl"


def train() -> dict[str, object]:
    iris = load_iris()
    features = iris.data[:, :3]
    pipeline = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            (
                "classifier",
                LogisticRegression(max_iter=200, random_state=42, solver="liblinear"),
            ),
        ]
    )
    pipeline.fit(features, iris.target)
    return {
        "model": pipeline,
        "model_version": MODEL_VERSION,
        "feature_names": list(iris.feature_names[:3]),
        "target_names": list(iris.target_names),
    }


def main() -> None:
    artifact = train()
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    with MODEL_PATH.open("wb") as model_file:
        pickle.dump(artifact, model_file)
    print(f"Wrote model artifact to {MODEL_PATH.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
