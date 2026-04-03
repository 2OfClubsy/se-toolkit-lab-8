# Lab 8 — Report

## Task 1A — Bare agent

**Question: "What is the agentic loop?"**

The agentic loop is the core cycle that an autonomous AI agent follows to accomplish tasks:

1. **Perceive** — Observe the environment: read user input, check tool outputs, review file state, fetch data from APIs, etc.
2. **Think / Plan** — Reason about what to do next. This includes deciding which tools to call, what order to call them in, and whether more information is needed.
3. **Act** — Execute the chosen action: call a tool, write a file, run a command, send a message, etc.
4. **Observe** — Receive the result of the action (success, error, output data) and feed it back into the loop.

The loop repeats until the task is complete or a stopping condition is met.

**Question: "What labs are available in our LMS?"**

The agent does not return real backend data at this stage without the MCP server configured. It may inspect local repo files and answer from documentation instead of the live LMS.

---

## Task 1B — Agent with LMS tools

**Question: "What labs are available?"**

The agent returned real lab names from the backend:

| # | Lab |
|---|-----|
| 1 | Lab 01 – Products, Architecture & Roles |
| 2 | Lab 02 — Run, Fix, and Deploy a Backend Service |
| 3 | Lab 03 — Backend API: Explore, Debug, Implement, Deploy |
| 4 | Lab 04 — Testing, Front-end, and AI Agents |
| 5 | Lab 05 – Data Pipeline and Analytics Dashboard |
| 6 | Lab 06 – Build Your Own Agent |
| 7 | Lab 07 – Build a Client with an AI Coding Agent |
| 8 | lab-08 |

**Question: "Is the LMS backend healthy?"**

Yes, the LMS backend is healthy. It's currently tracking **56 items**.

---

## Task 1C — Skill prompt

**Question: "Show me the scores" (without specifying a lab)**

The agent correctly asked which lab I wanted to see scores for, listing all 8 available labs with their titles. It did not return raw data — instead it prompted for lab selection as expected.

Response: "Which lab would you like to see the scores for?" followed by the numbered list of all available labs.
