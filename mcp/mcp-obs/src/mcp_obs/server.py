"""Stdio MCP server exposing observability tools (logs + traces)."""

from __future__ import annotations

import asyncio
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool
from pydantic import BaseModel, Field

from mcp_obs.observability import LogsQueryClient, TraceQueryClient
from mcp_obs.settings import get_logs_endpoint, get_traces_endpoint


# --- Tool input models ---

class SearchLogsInput(BaseModel):
    logsql_query: str = Field(description="LogsQL expression, e.g. '_time:10m severity:ERROR'")
    max_entries: int = Field(default=50, description="Maximum number of log lines to return")


class CountErrorsInput(BaseModel):
    service_name: str | None = Field(default=None, description="Filter by service, e.g. 'Learning Management Service'")
    window_minutes: int = Field(default=60, description="Look-back period in minutes")


class ListTracesInput(BaseModel):
    service_name: str | None = Field(default=None, description="Filter traces by service")
    max_traces: int = Field(default=10, description="Maximum traces to list")


class GetTraceInput(BaseModel):
    trace_id: str = Field(description="Unique trace identifier to retrieve")


# --- Server factory ---

def build_server(logs: LogsQueryClient, traces: TraceQueryClient) -> Server:
    server = Server("observability")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name="obs_logs_search",
                description="Query structured logs with LogsQL. Use _time: for windows, severity:ERROR for failures, service.name: to scope.",
                inputSchema=SearchLogsInput.model_json_schema(),
            ),
            Tool(
                name="obs_error_tally",
                description="Count error-level log records within a rolling time window. Optionally scope to one service.",
                inputSchema=CountErrorsInput.model_json_schema(),
            ),
            Tool(
                name="obs_traces_recent",
                description="List the most recent traces. Filter by service name if needed.",
                inputSchema=ListTracesInput.model_json_schema(),
            ),
            Tool(
                name="obs_trace_detail",
                description="Retrieve a full trace by its ID, showing every span with timing and service info.",
                inputSchema=GetTraceInput.model_json_schema(),
            ),
        ]

    @server.call_tool()
    async def call_tool(tool_name: str, arguments: dict[str, Any] | None) -> list[TextContent]:
        params = arguments or {}
        try:
            match tool_name:
                case "obs_logs_search":
                    parsed = SearchLogsInput(**params)
                    output = await logs.run_query(parsed.logsql_query, parsed.max_entries)
                case "obs_error_tally":
                    parsed = CountErrorsInput(**params)
                    output = await logs.tally_errors(parsed.service_name, parsed.window_minutes)
                case "obs_traces_recent":
                    parsed = ListTracesInput(**params)
                    output = await traces.fetch_recent(parsed.service_name, parsed.max_traces)
                case "obs_trace_detail":
                    parsed = GetTraceInput(**params)
                    output = await traces.fetch_by_id(parsed.trace_id)
                case _:
                    output = f"Unknown tool: {tool_name}"
        except Exception as exc:
            output = f"Error: {type(exc).__name__}: {exc}"
        return [TextContent(type="text", text=output)]

    return server


async def main() -> None:
    logs_client = LogsQueryClient(get_logs_endpoint())
    traces_client = TraceQueryClient(get_traces_endpoint())

    server = build_server(logs_client, traces_client)

    async with stdio_server() as (read_stream, write_stream):
        init_options = server.create_initialization_options()
        await server.run(read_stream, write_stream, init_options)


if __name__ == "__main__":
    asyncio.run(main())
