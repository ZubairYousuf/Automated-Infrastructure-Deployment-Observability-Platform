# Operations runbook

## API unavailable
Run `docker compose ps` and `docker compose logs --tail=100 api nginx`. Check `curl -v http://localhost:8080/health/ready` and the API health status. Check Prometheus target status.

## Prometheus target down
Inspect `docker compose logs prometheus`, then check service DNS and target names in infra/prometheus/prometheus.yml. Confirm API /metrics is available on the internal Docker network.

## Grafana dashboard empty
Confirm Prometheus datasource provisioning, time range, and successful scrapes. Generate sample traffic with `bash scripts/load-test.sh`.

## Rollback
The deployment script backs up .env and restores the prior APP_IMAGE if the readiness gate fails. Inspect logs and verify the previous image remains available. Never delete the previous image before recovery is confirmed.

## Security
Rotate any leaked credentials immediately. Keep .env out of Git. Restrict server and monitoring ports.
