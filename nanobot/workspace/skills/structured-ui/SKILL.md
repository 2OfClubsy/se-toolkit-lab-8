---
name: structured-ui
description: Deliver interactive choice/confirm messages on compatible channels
always: true
---

# Interactive UI Skill

Send interactive messages when the user faces a real decision between valid options.

## When to use

- Reach for `mcp_webchat_ui_message` instead of plain text lists when presenting multiple concrete options.
- Apply to selection scenarios: picking a lab, filtering results, choosing an action, or clarifying vague requests.
- If only one reasonable next step exists, reply normally — don't force an interactive prompt.
- Fall back to a short text question if the current channel doesn't support interactive widgets.

## Message types

- `choice` — present multiple options
- `confirm` — yes/no confirmation
- `composite` — combine brief explanation with an interactive component

## Guidelines

- Skip preamble text like "Let me check" before the interactive element. Send the choice directly, or wrap context + choice in a single `composite` payload.
- Pull the active `chat_id` from session runtime context and include it so the message routes to the correct WebSocket client.
