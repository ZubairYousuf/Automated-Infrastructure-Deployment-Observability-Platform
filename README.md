# Automated Infrastructure Deployment & Observability Platform

A medium-sized DevOps portfolio lab featuring FastAPI, Docker Compose, NGINX, GitHub Actions, Ansible, Prometheus, Grafana, Alertmanager, and health-gated deployment rollback.

## Features

- FastAPI service with health checks, task API, and Prometheus metrics
- Docker Compose with NGINX reverse proxy and resource constraints
- CI checks and container image publishing workflows
- Ansible Ubuntu deployment playbook
- Prometheus monitoring, Grafana dashboards, and alert rules
- Health-checked release and rollback scripts

## Local quick start

```bash
cp .env.example .env
docker compose up --build -d
curl -f http://localhost:8080/health/ready
```

The complete project source is being prepared for publication. This README alone is not a runnable deployment.

## Scope

Educational infrastructure/portfolio implementation, not a production-hardened service. Do not claim live uptime or performance results without running and measuring them.
