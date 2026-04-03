"""HTTP clients for VictoriaLogs and VictoriaTraces query APIs."""

from __future__ import annotations

import httpx


class LogsQueryClient:
    """Wraps the VictoriaLogs HTTP interface for log searches and error counts."""

    def __init__(self, base_url: str) -> None:
        self._base = base_url.rstrip("/")

    async def run_query(self, logsql: str, max_entries: int = 50) -> str:
        """Execute a LogsQL query and return matching log lines."""
        async with httpx.AsyncClient(timeout=30) as session:
            response = await session.get(
                f"{self._base}/select/logsql/query",
                params={"query": logsql, "limit": max_entries},
            )
            response.raise_for_status()
            entries = response.text.strip().split("\n")
            if not entries or entries == [""]:
                return "No matching log entries found."
            return "\n".join(entries[:max_entries])

    async def tally_errors(self, service_name: str | None = None, window_minutes: int = 60) -> str:
        """Count severity:ERROR records within a rolling time window."""
        time_clause = f"_time:{window_minutes}m"
        filters = [time_clause, "severity:ERROR"]
        if service_name:
            filters.append(f'service.name:"{service_name}"')
        logsql = " ".join(filters)
        async with httpx.AsyncClient(timeout=30) as session:
            response = await session.get(
                f"{self._base}/select/logsql/query",
                params={"query": logsql, "limit": 1000},
            )
            response.raise_for_status()
            lines = [line for line in response.text.strip().split("\n") if line.strip()]
            total = len(lines)
            return f"Detected {total} error record(s) across the last {window_minutes} minutes."


class TraceQueryClient:
    """Wraps the VictoriaTraces Jaeger-compatible API for trace inspection."""

    def __init__(self, base_url: str) -> None:
        self._base = base_url.rstrip("/")

    async def fetch_recent(self, service_name: str | None = None, max_traces: int = 10) -> str:
        """Return a summary of the most recent traces."""
        async with httpx.AsyncClient(timeout=30) as session:
            params: dict[str, str | int] = {"limit": max_traces}
            if service_name:
                params["service"] = service_name
            response = await session.get(
                f"{self._base}/select/jaeger/api/traces",
                params=params,
            )
            response.raise_for_status()
            payload = response.json()
            traces = payload.get("data", [])
            if not traces:
                return "No traces found."
            summaries: list[str] = []
            for trace in traces[:max_traces]:
                trace_id = trace.get("traceID", "unknown")
                spans = trace.get("spans", [])
                services: set[str] = set()
                for span in spans:
                    proc = span.get("process", {})
                    services.add(proc.get("serviceName", "unknown"))
                summaries.append(
                    f"Trace {trace_id}: {len(spans)} span(s) — services: {', '.join(sorted(services))}"
                )
            return "\n".join(summaries)

    async def fetch_by_id(self, trace_id: str) -> str:
        """Retrieve the full span hierarchy for a single trace."""
        async with httpx.AsyncClient(timeout=30) as session:
            response = await session.get(
                f"{self._base}/select/jaeger/api/traces/{trace_id}",
            )
            response.raise_for_status()
            payload = response.json()
            traces = payload.get("data", [])
            if not traces:
                return f"No trace found for ID: {trace_id}"
            trace = traces[0]
            spans = trace.get("spans", [])
            lines: list[str] = [
                f"Trace ID: {trace.get('traceID', 'unknown')}",
                f"Total spans: {len(spans)}",
                "",
            ]
            for span in spans:
                operation = span.get("operationName", "?")
                proc = span.get("process", {})
                service = proc.get("serviceName", "?")
                duration_ms = span.get("duration", 0) / 1000
                parent = span.get("references", [{}])[0].get("spanID")
                parent_label = f" (child of {parent})" if parent else " (root)"
                lines.append(f"  [{service}] {operation} — {duration_ms:.1f}ms{parent_label}")
            return "\n".join(lines)
