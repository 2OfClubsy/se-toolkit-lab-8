"""Resolve configuration for observability service endpoints."""

import os


def get_logs_endpoint() -> str:
    """Return VictoriaLogs base URL from environment or default."""
    return os.environ.get("NANOBOT_VICTORIALOGS_URL", "http://localhost:9428")


def get_traces_endpoint() -> str:
    """Return VictoriaTraces base URL from environment or default."""
    return os.environ.get("NANOBOT_VICTORIATRACES_URL", "http://localhost:10428")
