#!/bin/bash
# Sync wiki-content into OtterWiki. Run this from the project root after docker compose up.
# Use this in your Forge/server deploy script instead of direct cp (avoids permission errors).

set -e
CONTAINER=$(docker compose ps -q otterwiki 2>/dev/null | head -1)
[ -z "$CONTAINER" ] && CONTAINER=$(docker ps -qf "name=otterwiki" | head -1)
[ -z "$CONTAINER" ] && { echo "OtterWiki container not found"; exit 1; }

# Wait for container to be ready
sleep 3

# Copy files into container (avoids host permission issues)
docker cp wiki-content/Home.md "$CONTAINER:/app-data/repository/home.md"
docker cp wiki-content/apis "$CONTAINER:/app-data/repository/"
[ -d wiki-content/functions ] && docker cp wiki-content/functions "$CONTAINER:/app-data/repository/"
[ -d wiki-content/agents ] && docker cp wiki-content/agents "$CONTAINER:/app-data/repository/"
[ -d wiki-content/mcp_servers ] && docker cp wiki-content/mcp_servers "$CONTAINER:/app-data/repository/"
[ -d wiki-content/middlewares ] && docker cp wiki-content/middlewares "$CONTAINER:/app-data/repository/"
[ -d wiki-content/tables ] && docker cp wiki-content/tables "$CONTAINER:/app-data/repository/"
[ -d wiki-content/tasks ] && docker cp wiki-content/tasks "$CONTAINER:/app-data/repository/"
[ -d wiki-content/shunyaku ] && docker cp wiki-content/shunyaku "$CONTAINER:/app-data/repository/"

# Commit inside container (fix safe.directory + ensure git identity for fresh containers)
docker exec "$CONTAINER" sh -c '
  git config --global --add safe.directory /app-data/repository
  git config --global user.email "deploy@wiki" 2>/dev/null || true
  git config --global user.name "Deploy" 2>/dev/null || true
  cd /app-data/repository && git add -A && git diff --cached --quiet || git commit -m "sync from GitHub"
'
