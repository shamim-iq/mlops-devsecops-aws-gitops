from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_returns_ok() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_predict_returns_prediction() -> None:
    response = client.post(
        "/predict",
        json={"feature_a": 1.0, "feature_b": 1.0, "feature_c": 0.0},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["prediction"] == 1
    assert body["model_version"] == "baseline-0.1.0"
    assert body["score"] == 0.8


def test_metrics_exposes_prometheus_output() -> None:
    response = client.get("/metrics")

    assert response.status_code == 200
    assert "prediction_api_requests_total" in response.text
