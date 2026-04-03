---
name: observability
description: Investigate system errors using VictoriaLogs and VictoriaTraces
always: true
---

# Observability Skill

You have access to log and trace query tools backed by VictoriaLogs and VictoriaTraces. Use them to diagnose failures when the user asks about errors, outages, or system health.

## Available Tools

| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `obs_error_tally` | Count error records in a time window | `service_name` (optional), `window_minutes` |
| `obs_logs_search` | Run a LogsQL query against structured logs | `logsql_query`, `max_entries` |
| `obs_traces_recent` | List recent traces, optionally by service | `service_name` (optional), `max_traces` |
| `obs_trace_detail` | Fetch full span hierarchy for one trace | `trace_id` |

## Investigation Strategy

When the user asks **"What went wrong?"**, **"Any errors?"**, or **"Check system health"**:

1. **Start with the error count** — call `obs_error_tally` on a narrow recent window (e.g., 10 minutes). This tells you whether there are errors at all.
2. **If errors exist, search the logs** — call `obs_logs_search` scoped to the most likely failing service. Extract a `trace_id` from the log output if one is present.
3. **Fetch the trace** — call `obs_trace_detail` with the extracted `trace_id` to see the full request path and pinpoint where it failed.
4. **Summarize** — give a short explanation that references both the log evidence and the trace evidence. Name the affected service and the root failing operation. Do not dump raw JSON.

## Response guidelines

- Lead with the conclusion (healthy / degraded / failing)
- Cite specific numbers: "3 errors in the last 10 minutes"
- Reference trace evidence: "Trace abc123 shows the request failed at the database query step"
- Keep it concise — 2-4 sentences for a healthy system, slightly more for a failure

## Time windows

- For scoped questions like "any LMS errors in the last 10 minutes?", use `window_minutes: 10` and filter by the LMS service name
- For broader questions like "any errors in the last hour?", use `window_minutes: 60`
- Always prefer the narrowest window that answers the question to avoid surfacing stale historical errors
