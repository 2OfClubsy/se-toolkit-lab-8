# Nanobot Agent

Custom nanobot setup for LMS integration with WebSocket web client support.

## Structure

- `config.json` — agent configuration (LLM provider, MCP servers)
- `entrypoint.py` — Docker entrypoint that resolves env vars into config
- `workspace/` — agent skills, memory, and session data
- `Dockerfile` — multi-stage build for containerized deployment

## Usage

### Local development

```bash
cd nanobot
uv sync
uv run nanobot agent --logs --session cli:dev -c ./config.json
```

### Docker deployment

```bash
docker compose --env-file .env.docker.secret build nanobot
docker compose --env-file .env.docker.secret up -d nanobot
```
