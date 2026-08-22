# Prediction App Functionality

The prediction app is a small FastAPI service that demonstrates how an ML model becomes a deployable application artifact. It trains a lightweight classifier, saves it as `model.pkl`, loads it when the API starts, and exposes endpoints that can be tested, containerized, deployed, monitored, and rolled back.

## What It Predicts

The model uses the built-in scikit-learn Iris dataset. Each row contains numeric flower measurements, and the target is the flower class.

The API accepts three numeric fields:

| API field | Purpose |
|---|---|
| `feature_a` | First model feature |
| `feature_b` | Second model feature |
| `feature_c` | Third model feature |

The API returns:

| Field | Purpose |
|---|---|
| `prediction` | Predicted class id |
| `score` | Highest class probability |
| `model_version` | Version stored with the model artifact |

The model is intentionally small. Its purpose is to provide a realistic ML-serving workload for the MLOps demo, not to optimize flower classification accuracy.

## Training Flow

Training runs from:

```text
scripts/train_model.py
```

The script:

```text
loads the Iris dataset
  -> selects the first three numeric features
  -> scales features with StandardScaler
  -> trains LogisticRegression
  -> packages the pipeline, model version, feature names, and target names
  -> writes app/model/model.pkl
```

The artifact version is:

```text
iris-logreg-0.1.0
```

The trained model is a scikit-learn pipeline, so preprocessing and classification are stored together. The API can pass raw numeric fields to the pipeline and receive class probabilities.

## Inference Flow

The API loads `app/model/model.pkl` when `app/main.py` starts.

`POST /predict` does this:

```text
validates the JSON request with Pydantic
  -> builds a one-row feature array
  -> calls predict_proba for class probabilities
  -> calls predict for the class id
  -> returns prediction, score, and model_version
```

The score is the highest class probability, rounded for a stable response.

## Runtime Endpoints

| Endpoint | Purpose |
|---|---|
| `GET /health` | Health check for local tests, container checks, and Kubernetes probes |
| `POST /predict` | Model prediction endpoint |
| `GET /metrics` | Prometheus metrics endpoint |

The metrics endpoint exposes request counters and prediction latency. Prometheus and Argo Rollouts can later use these signals to decide whether a canary release should promote or roll back.

## Why This App Fits The Demo

The app is CPU-only, quick to build, and small enough for a short-lived EKS demo. It still exercises the full lifecycle:

```text
train model
  -> save artifact
  -> serve with FastAPI
  -> test and lint
  -> audit dependencies
  -> build Docker image
  -> deploy with Helm and Argo CD
  -> validate rollout with Prometheus
```
