# Argo CD Install Notes

Install Argo CD only after the EKS cluster exists. The application source path for the prediction API is `k8s/apps/prediction-api/overlays/prod`.

Do not connect Argo CD with write access to the repository. CI and CD own repository mutations, and Argo CD only reconciles desired state into the cluster.
