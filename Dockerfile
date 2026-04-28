FROM python:3.12-slim

WORKDIR /app

# Install uv for fast package management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy project files
COPY pyproject.toml server.py vault_bridge.py state.json ./

# Install dependencies
RUN uv pip install --system fastmcp>=2.0 uvicorn

# WELL env vars
ENV WELL_VAULT_PATH=/root/arifOS/core/vault999/well_ledger.jsonl
ENV WELL_STATE_PATH=/root/WELL/state.json
ENV LOG_LEVEL=info

EXPOSE 8083

CMD ["python", "server.py"]
