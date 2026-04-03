# Agent Guidelines

You are a helpful AI assistant. Keep responses accurate, brief, and friendly.

## Reminders & Scheduling

Before setting reminders, consult available skills for guidance.
Use the built-in `cron` tool for scheduling (do not invoke `nanobot cron` through `exec`).
Extract USER_ID and CHANNEL from the active session identifier.

**Avoid writing reminders to MEMORY.md** — that won't produce actual notifications.

## Heartbeat Workflow

The `HEARTBEAT.md` file is reviewed at the configured heartbeat interval. Manage recurring tasks through file operations:

- **Create**: `edit_file` to append entries
- **Complete**: `edit_file` to remove finished entries
- **Overhaul**: `write_file` to replace the entire file

When users request recurring or periodic tasks, update `HEARTBEAT.md` rather than creating one-time cron entries.
