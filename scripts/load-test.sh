#!/usr/bin/env bash
set -euo pipefail
BASE_URL="${1:-http://localhost:8080}"
COUNT="${2:-100}"
if ! [[ "$COUNT" =~ ^[0-9]+$ ]] || (( COUNT < 1 || COUNT > 10000 )); then
  echo "Count must be between 1 and 10000" >&2; exit 2
fi
for ((i=1; i<=COUNT; i++)); do
  curl -fsS "$BASE_URL/health/ready" >/dev/null
done
echo "Sent $COUNT successful requests to $BASE_URL"
