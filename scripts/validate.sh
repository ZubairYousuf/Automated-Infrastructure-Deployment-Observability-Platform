#!/usr/bin/env bash
set -euo pipefail
python3 -m compileall -q app
python3 -m pytest -q app/tests
python3 -m ruff check app
if command -v docker >/dev/null 2>&1; then
  GRAFANA_ADMIN_PASSWORD=test-not-a-production-password docker compose config --quiet
fi
