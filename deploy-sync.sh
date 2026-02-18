#!/bin/bash
# Sync wiki-content into OtterWiki. Run with: bash deploy-sync.sh (no chmod needed)
# Uses docker cp/exec only - no write access to app-data on host required.

set -e
CONTAINER=$(docker compose ps -q otterwiki 2>/dev/null | head -1)
[ -z "$CONTAINER" ] && CONTAINER=$(docker ps -qf "name=otterwiki" | head -1)
[ -z "$CONTAINER" ] && { echo "OtterWiki container not found"; exit 1; }

sleep 3

# Copy everything from wiki-content into container (no host write permissions needed)
docker cp wiki-content/Home.md "$CONTAINER:/app-data/repository/home.md" 2>/dev/null || true
for item in wiki-content/*; do
  [ -e "$item" ] || continue
  [ "$(basename "$item")" = "Home.md" ] && continue
  docker cp "$item" "$CONTAINER:/app-data/repository/" 2>/dev/null || true
done

# Commit inside container
docker exec "$CONTAINER" sh -c '
  git config --global --add safe.directory /app-data/repository 2>/dev/null || true
  git config --global user.email "deploy@wiki" 2>/dev/null || true
  git config --global user.name "Deploy" 2>/dev/null || true
  cd /app-data/repository && git add -A && (git diff --cached --quiet || git commit -m "sync from GitHub")
'
