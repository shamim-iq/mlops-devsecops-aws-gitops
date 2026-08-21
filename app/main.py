import pickle
from time import perf_counter
from pathlib import Path

from fastapi import FastAPI
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from pydantic import BaseModel, Field
from starlette.responses import Response


REQUEST_COUNT = Counter(
    "prediction_api_requests_total",
    "Total prediction API requests.",
    ["endpoint", "method", "status"],
)
PREDICTION_LATENCY = Histogram(
    "prediction_api_prediction_seconds",
    "Prediction request latency in seconds.",
)
MODEL_PATH = Path(__file__).resolve().parent / "model" / "model.pkl"


def load_model_artifact() -> dict[str, object]:
    with MODEL_PATH.open("rb") as model_file:
        return pickle.load(model_file)


MODEL_ARTIFACT = load_model_artifact()
MODEL = MODEL_ARTIFACT["model"]
MODEL_VERSION = str(MODEL_ARTIFACT["model_version"])

app = FastAPI(title="MLOps DevSecOps Prediction API", version="0.1.0")


class PredictionRequest(BaseModel):
    feature_a: float = Field(..., description="First numeric feature.")
    feature_b: float = Field(..., description="Second numeric feature.")
    feature_c: float = Field(..., description="Third numeric feature.")


class PredictionResponse(BaseModel):
    prediction: int
    score: float
    model_version: str


@app.get("/health")
def health() -> dict[str, str]:
    REQUEST_COUNT.labels(endpoint="/health", method="GET", status="200").inc()
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionResponse)
def predict(payload: PredictionRequest) -> PredictionResponse:
    started = perf_counter()
    features = [[payload.feature_a, payload.feature_b, payload.feature_c]]
    probabilities = MODEL.predict_proba(features)[0]
    prediction = int(MODEL.predict(features)[0])
    score = float(max(probabilities))
    PREDICTION_LATENCY.observe(perf_counter() - started)
    REQUEST_COUNT.labels(endpoint="/predict", method="POST", status="200").inc()
    return PredictionResponse(prediction=prediction, score=round(score, 4), model_version=MODEL_VERSION)


@app.get("/metrics")
def metrics() -> Response:
    REQUEST_COUNT.labels(endpoint="/metrics", method="GET", status="200").inc()
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
