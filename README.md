# Minimal MLOps DevSecOps Pipeline

This repository contains the implementation for a small MLOps and DevSecOps demo on AWS. It holds the FastAPI prediction service, tests, Docker build, Terraform infrastructure, GitHub Actions workflows, and Kubernetes desired state used by Argo CD and Argo Rollouts.

No AWS resources are deployed from this repository until the owner reviews a Terraform plan and runs the apply command with the deployment profile.

## Local App

Create a virtual environment, install dependencies, and run tests.

```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
pytest
```

Run the API locally.

```bash
uvicorn app.main:app --reload
```

Endpoints:

```text
GET /health
POST /predict
GET /metrics
```

## Repository Layout

```text
app/          FastAPI prediction service
tests/        API tests
terraform/    AWS infrastructure as code
k8s/          Kubernetes desired state for Argo CD
.github/      GitHub Actions workflows
docs/         project notes
```
