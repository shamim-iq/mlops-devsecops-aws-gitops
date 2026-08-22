# Prediction API Base

This Kustomize base defines the namespace, internal service, Argo Rollouts `Rollout`, and Prometheus `AnalysisTemplate` for the FastAPI prediction API.

The base image name is `prediction-api:local`. The production overlay replaces it with the ECR image URI and tag after CI publishes an approved image.
