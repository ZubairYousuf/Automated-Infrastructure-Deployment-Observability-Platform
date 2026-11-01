#!/usr/bin/env bash
set -Eeuo pipefail
if [[ $# -ne 1 ]]; then echo "usage: $0 <immutable-image-ref>" >&2; exit 2; fi
NEW_IMAGE="$1"
BASE_DIR="${CLOUDOPS_DIR:-/opt/cloudops}"
cd "$BASE_DIR"
if [[ ! -f .env ]]; then echo "Missing $BASE_DIR/.env" >&2; exit 1; fi
CURRENT_IMAGE="$(grep -E '^APP_IMAGE=' .env | tail -1 | cut -d= -f2- || true)"
if [[ -z "$CURRENT_IMAGE" ]]; then echo "APP_IMAGE missing" >&2; exit 1; fi
if [[ "$CURRENT_IMAGE" == "$NEW_IMAGE" ]]; then echo "Already deployed $NEW_IMAGE"; exit 0; fi
cp .env .env.predeploy
rollback() {
  echo "Release failed, restoring previous image: $CURRENT_IMAGE" >&2
  mv -f .env.predeploy .env
  docker compose up -d --no-deps --force-recreate api
  docker compose ps api
}
trap rollback ERR
docker pull "$NEW_IMAGE"
python3 - "$NEW_IMAGE" <<'PYUPDATE'
from pathlib import Path
import sys
p = Path('.env')
lines = p.read_text().splitlines()
lines = [f'APP_IMAGE={sys.argv[1]}' if line.startswith('APP_IMAGE=') else line for line in lines]
p.write_text('\n'.join(lines) + '\n')
PYUPDATE
docker compose up -d --no-deps --force-recreate api
for attempt in $(seq 1 30); do
  if docker compose exec -T api python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health/ready',timeout=2)" >/dev/null 2>&1; then
    rm -f .env.predeploy
    trap - ERR
    echo "Deployment healthy: $NEW_IMAGE"
    exit 0
  fi
  sleep 2
done
false
