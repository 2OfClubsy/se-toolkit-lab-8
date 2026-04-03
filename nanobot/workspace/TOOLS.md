# Tool Notes

Tool signatures are passed automatically through function calling.
This file captures non-obvious constraints and patterns.

## exec — Guardrails

- Commands respect a configurable timeout (60s default)
- Hazardous commands are blocked (recursive deletes, disk formatting, shutdown, etc.)
- Output is capped at 10,000 characters
- The `restrictToWorkspace` setting can confine file access to the workspace root

## cron — Scheduled Jobs

- Refer to the cron skill for add/list/remove operations.
