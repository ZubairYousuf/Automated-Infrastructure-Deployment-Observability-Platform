# Architecture

The CloudOps platform demonstrates a single-host container deployment and observability stack.

## Request flow
Client -> NGINX (port 8080) -> FastAPI (internal port 8000). NGINX blocks public /metrics access.

## Monitoring flow
Prometheus scrapes FastAPI /metrics and node-exporter on an internal Docker network. Grafana uses Prometheus as its provisioned datasource. Alertmanager receives configured Prometheus alerts, but no external notification destination is enabled by default.

## Release flow
GitHub Actions tests and builds the API image. A separate workflow publishes immutable SHA-tagged images to GHCR. Ansible configures an Ubuntu host. The deploy script replaces the running image, checks readiness, and rolls back on failed health checks.

## Limitations
This is a single-host educational lab, not an HA platform. Task data is in memory and resets on restart. HTTPS and real alert receivers require environment-specific configuration. Host monitoring through node-exporter may require privileged host mounts.
