# Publishing and validation

This repository contains an educational single-host DevOps platform. After publishing, check GitHub Actions CI results before presenting it as tested.

## Local smoke test
```bash
cp .env.example .env
# Set a unique GRAFANA_ADMIN_PASSWORD
docker compose up --build -d
curl -f http://localhost:8080/health/ready
docker compose ps
```

## Useful links
- API: http://localhost:8080
- Grafana: http://127.0.0.1:3000
- Prometheus: http://127.0.0.1:9090
- Alertmanager: http://127.0.0.1:9093

## Notes
No cloud infrastructure or production uptime is claimed. Configure notifications and HTTPS separately.
