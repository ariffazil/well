#!/bin/bash
# WELL Deployment Script — 2026.05.08
# Builds, tags, pushes, and rolls out the WELL MCP server.

set -euo pipefail

TAG="${1:-$(git rev-parse --short HEAD)}"
IMAGE="ghcr.io/ariffazil/well:${TAG}"

echo "=== WELL Deploy ==="
echo "Tag: ${TAG}"
echo "Image: ${IMAGE}"

# Build
echo "[1/4] Building Docker image..."
docker build -t "well:${TAG}" .

# Tag for registry
echo "[2/4] Tagging for GHCR..."
docker tag "well:${TAG}" "${IMAGE}"

# Push (requires GHCR login)
echo "[3/4] Pushing to GHCR..."
if docker push "${IMAGE}"; then
    echo "Push OK"
else
    echo "Push failed — ensure 'docker login ghcr.io' is done"
    exit 1
fi

# Update compose and roll out
echo "[4/4] Rolling out via compose..."
cd /root/compose
sed -i "s|image: ghcr.io/ariffazil/well:.*|image: ${IMAGE}|" docker-compose.yml
docker compose up -d --no-deps --build well
docker compose ps well
docker compose logs --tail=20 well

echo "=== Deploy complete ==="
echo "Health check: curl https://well.arif-fazil.com/health"
