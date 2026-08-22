# Prediction API Helm Chart

This chart renders the prediction API namespace, service, Argo Rollouts `Rollout`, and Prometheus `AnalysisTemplate`.

Use `values.yaml` for safe local defaults. Use `values-prod.yaml` for the production image fields that CD updates after the approved image is pushed to ECR.

```bash
helm template prediction-api ./k8s/apps/prediction-api/chart -f ./k8s/apps/prediction-api/chart/values-prod.yaml
```

Argo CD should use this chart path:

```text
k8s/apps/prediction-api/chart
```
