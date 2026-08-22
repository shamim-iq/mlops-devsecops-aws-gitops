# Argo Rollouts Install Notes

Install Argo Rollouts before applying the prediction API manifests because the app uses the `argoproj.io/v1alpha1` `Rollout` and `AnalysisTemplate` resources.

The demo uses one replica and a small canary step so it fits the CPU-only EKS node candidate.
