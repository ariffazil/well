FROM python:3.12-slim

WORKDIR /app

# Install uv for fast package management
# NOTE: Pin to specific version for supply-chain integrity.
# For full reproducibility, replace with digest-pinned image.
COPY --from=ghcr.io/astral-sh/uv:0.6.16 /uv /usr/local/bin/uv

# Copy project files
COPY pyproject.toml server.py vault_bridge.py state.json ./

# Install dependencies
RUN uv pip install --system fastmcp>=2.0 uvicorn

# Create non-root user for runtime security
RUN useradd -m -u 1000 welluser && chown -R welluser:welluser /app
USER welluser

# WELL env vars
ENV WELL_VAULT_PATH=/tmp/well_ledger.jsonl
ENV WELL_STATE_PATH=/app/state.json
ENV HOST=0.0.0.0
ENV PORT=8083
ENV LOG_LEVEL=info

EXPOSE 8083

CMD ["python", "server.py"]
