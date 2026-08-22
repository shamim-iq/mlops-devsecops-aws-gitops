# Prediction API Production Overlay

Argo CD should use this path as the application source:

```text
k8s/apps/prediction-api/overlays/prod
```

The overlay keeps `<ecr-repository-uri>` and `<image-tag>` placeholders until Terraform creates ECR and CD writes the approved image version.
