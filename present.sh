#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
test -f dist/index.html || { echo 'Build first: npm ci && npm run build' >&2; exit 1; }
command -v node >/dev/null || { echo 'Node.js is required to serve the offline deck.' >&2; exit 1; }
node scripts/serve.mjs &
presentation_server_pid=$!
trap 'kill "$presentation_server_pid" 2>/dev/null || true' EXIT INT TERM
for attempt in {1..50}; do
  kill -0 "$presentation_server_pid" 2>/dev/null || exit 1
  if curl --silent --fail "http://127.0.0.1:${PORT:-3030}/" >/dev/null; then break; fi
  sleep 0.1
done
curl --silent --fail "http://127.0.0.1:${PORT:-3030}/" >/dev/null || { echo 'Server did not become ready.' >&2; exit 1; }
if command -v xdg-open >/dev/null; then xdg-open "http://127.0.0.1:${PORT:-3030}/" >/dev/null 2>&1 || true
elif command -v open >/dev/null; then open "http://127.0.0.1:${PORT:-3030}/" || true; fi
wait "$presentation_server_pid"
