---
name: di-agent-bug-report
description: Generates a Markdown bug report for an IBM watsonx.data integration session. User can invoke directly. The agent MUST propose it (and must wait for explicit acceptance) after 3 or more consecutive calls to the same tool or the same sequence of tools result in a failure or the same error. Skip for non-watsonx.data integration sessions.
---

# DI Agent Bug Report — IBM watsonx.data integration Session

Captures the current AI-agent session into a Markdown report so the watsonx.data integration skill authors can debug what went wrong (or confirm what worked) while the agent was creating, running, or managing a watsonx.data integration flow. The skill is agent-agnostic — do not assume any specific AI runtime, model, or session-file layout.

## When to Use

- **Manual:** the user explicitly asks to report a bug or files a bug report. Proceed directly — no confirmation needed.
- **Automatic (proposed, never silent — once per session):** the agent MUST propose this skill whenever the loop-detection rule fires. Strict triggering rules:

  1. **Loop-detection rule (primary trigger).** After every tool call, maintain a rolling call log that tracks the tool name(s) invoked. A "repeat" occurs when the agent calls the **same tool**, or the **same ordered sequence of tools in a single turn**, 3 or more consecutive times and each attempt produced the same error, the same failure status, or no meaningful change in the output. When the 3rd such repeat is detected:
     - Stop immediately — do not make a 4th attempt.
     - Propose the bug report: *"I've called `<tool(s)>` 3 times with the same result (<one-line error/symptom>). Want me to file a bug report? (yes / no)"*
     - Wait for an explicit reply before proceeding.
     - Examples that qualify:
       - Calling `compile_datastage_flow` 3 times and getting the same compile error each time.
       - Calling `create_job` → `run_job` → `get_job_run_logs` as a unit 3 consecutive times and receiving the same failure on each cycle.
       - Calling any single MCP tool 3 times in a row where the error message is identical or the output is structurally unchanged.
     - Examples that do **not** qualify:
       - 3 calls where the inputs or parameters differ meaningfully (the agent is genuinely trying different things).
       - A tool returning an empty-but-successful result (not an error).
  2. **One proposal per session.** Track that an automatic proposal has been issued and **do not issue another automatic proposal for the remainder of the session, regardless of subsequent failures**. The user can still invoke the skill manually — the cap applies only to the automatic path.
  3. **Ask, then wait.** Send the one short proposal message and run the workflow only if the user replies affirmatively. If the user declines or ignores, do not write a file. Either response (accept, decline, ignore) consumes the one-per-session proposal slot.

A session counts as watsonx.data integration-related when **any** of the following are true:
- a skill whose name starts with the `di-agent-` prefix was used,
- an MCP tool belonging to the Agentic Data Integration MCP server was called (identify by the server prefix on the namespaced tool name, e.g. `mcp__ibm-agentic-data-integration__*`),
- the user asked to create / edit / run / debug a watsonx.data integration flow or job.

## Arguments

- `--name <filename>` *(optional)* — override the output filename. Written under `agent/bug_reports/`; basename only. `.md` is appended if missing. Reject path separators and `..`. When omitted, use the default name (see Invariant 3).

## Invariants

1. **watsonx.data integration only.** If the session is not watsonx.data integration-related (per the signals above), do not write a file — print a one-line skip message and stop. Detect first, then decide.
2. **Mask all PII before writing.** Apply redaction to user text, assistant text, transcript entries, and error strings — before writing the file, not after. Do **not** redact skill names, tool names, error messages, schema/column names, user id, project ids, asset ids, flow ids, jobs ids or public dataset names — those are needed for debugging.
3. **One file per invocation.** Default path: `ibm-watsonx-data-integration-agent-skills/agent/bug_reports/watsonx_di_agent_bug_report_<YYYY-MM-DD>_<HH-MM-SS>_<session_name>.md`, where `<HH-MM-SS>` is the local 24-hour time and `<session_name>` is a short AI-generated slug summarizing the user's initial intent — lowercase, hyphen-separated, ASCII letters/digits only, ≤6 words, no skill names as filler. With `--name`, write to `.../bug_reports/<filename>.md` instead. Create `bug_reports/` if missing. If the target exists, ask before overwriting.
4. **Use the conversation as the source of truth.** Reconstruct the transcript from the actual messages and tool calls, not guesses.

## Workflow

### 1. Resolve session metadata

- `session_date`, `session_time`: today's date and current local time (formats per Invariant 3).
- `session_name`: slug derived from the opening user prompts (rules per Invariant 3).
- `agent_session_id`: the host agent runtime's session identifier. Try, in order: (1) the runtime's active transcript / log file — common patterns include `~/.claude/projects/<encoded-cwd>/<uuid>.jsonl` (Claude Code), `~/.cursor/...`, or any path the runtime advertises in its docs; if a matching `<uuid>.jsonl` exists and is the most-recently-modified, use the UUID from the filename; (2) a runtime-introspection / `whoami` tool, if the host exposes one. If neither resolves, record `null` and note which sources were tried. Never invent or guess.
- `session_info`: call the watsonx.data integration `get_session_info` MCP tool and capture its full output verbatim. Render the raw key/value payload (one bullet per field) into the **Session Info** section directly above `generated_at`. Do not try to extract a single id — pass through whatever the tool returns. If the tool is unavailable or errors, record one bullet `**Session Info:** _tool unavailable._` and continue.
- `llm`: name and version of the LLM powering the host agent runtime (e.g. `claude-opus-4-7`, `claude-sonnet-4-6`, `gpt-5.1`). Use the model identifier the runtime states in its own system prompt — the LLM knows what it is running on. If self-identification is not possible, fall back to a runtime-introspection tool or a model-related environment variable. Record as `<name>-<version>`; record `null` only if none of these resolve.
- Output filename: `--name` value (sanitized, `.md` appended) or the default from Invariant 3.

### 2. Build the transcript

Single chronological section combining every entry of the session. Walk the conversation in order and append one numbered entry per user message, assistant text response, skill invocation, and tool call. **All entries share one numbering sequence**, ordered strictly by when they occurred — turns and tool calls interleave naturally.

Per-entry shapes:

- **User / assistant turn** — bold pseudo-heading followed directly by a fenced `text` block holding the PII-redacted body. **Verbatim only**: render the actual text character-for-character (modulo PII redaction). No summaries, no paraphrasing, no bracketed narration like `[Invoked X skill, then …]`. For assistant turns, include the user-visible prose only — strip internal reasoning and raw tool-call JSON. If an assistant turn had no user-visible text (tool calls only), skip it — do **not** invent prose.

  ```
  **N. turn — <User | Assistant>**

  ```text
  <verbatim PII-redacted text of the turn, line breaks preserved>
  ```

- **Skill or tool call** — bold pseudo-heading with kind, name, status, then `**Input:**` and `**Output:**` bullets.

  ```
  **N. <skill | tool> — `<name>` — status: <ok | error | unknown>**

  - **Input:** <one-line summary — never the full payload>
  - **Output:**

    ```text
    <result, truncated to ~2000 chars; `_No output._` if none; failure messages go here>
  ```

Notes:

- Generic Read/Edit/Bash calls only appear when they are part of the watsonx flow.
- The **Description** section cites entries by their transcript number (`entry N`).

### 3. Call diagnostic tools and gather deeper signal

**Required.** Job-run status in the transcript only reports `completed` / `failed` plus a short summary — not enough to diagnose what actually happened. Before finalizing **Description** (step 4), call the following watsonx.data integration MCP tools whenever the relevant inputs are available from the session. Skip a tool only when its inputs are missing; never block on a failure; record each attempt (including errors) as its own transcript entry.

- **`get_job_run_logs`** — full log stream and event history for the latest job run. Cite specific warnings/errors (e.g. implicit type conversions, partition counts, per-stage `in → out` row counts) in the Description.
- **`retrieve_datastage_flow_code`** — the stored definition of the submitted flow, so the report reflects what actually ran (column types, predicates, joins).

The Description **must be informed by these tool outputs** — do not write the diagnosis from the surface-level run status alone.

### 4. Diagnose the session

Produces the **Description** section. Classify using the transcript (step 2) plus diagnostic data (step 3):

- **Success — produced rows.** Flow completed; output consistent with the source.
- **Success — vacuously empty.** Job ran cleanly; the source itself has 0 data rows. Outcome `success`; say so explicitly.
- **Success — expected zero output.** Flow logic legitimately yields no rows (anti-join, filter, etc.). Outcome `success` with an explanatory **Description**.
- **Failure.** Logs show errors, rows were silently dropped given a non-empty source, or the agent looped / mis-used a tool / produced an invalid flow. Cite the specific signal in **Description**.

**Description length: hard cap of 5–6 sentences.** State the outcome and the direct reason — what failed, where (cite transcript entries as `entry N`), and what the evidence says. No background, no narrative, no restating what the user asked for.

### 5. Write the Markdown file

Create `ibm-watsonx-data-integration-agent-skills/agent/bug_reports/` if missing, then write using the template below.

Formatting rules:

- **The very first line of the file must be `# IBM watsonx.data integration Agent Bug Report`.** No leading YAML/Markdown frontmatter, no leading `---` separator, no blank lines, no shebang, no metadata block above the H1. The file starts with the H1 and nothing else.
- **Do not insert horizontal-rule separators (`---`)** anywhere in the document. Section boundaries are conveyed by `##` headings alone — Markdown `---` lines render as horizontal rules and clutter the output.
- Section order is fixed: Session Info → Description → Transcript.
- Only two heading levels: `#` for the title, `##` for sections. No `###` anywhere — use bold pseudo-headings.
- One blank line between sections and around fenced code blocks. End with a single trailing newline.
- Code-fence multi-line outputs with language hints.
- Keep field labels bold (`**Input:**`, `**Output:**`, etc.).
- For empty sections, write a single italic line.

Template:

````markdown
# IBM watsonx.data integration Agent Bug Report

**Outcome:** [success | failure]

## Session Info

- **Agent Session ID:** `[uuid or null]`
- **LLM:** `[name-version, e.g. claude-opus-4-7, or null]`
- **`get_session_info`:** [render each field returned by the tool as its own indented bullet, verbatim — e.g. `session_id`, `client_type`, etc. If the tool errored or was unavailable, write `_tool unavailable._` instead.]
- **Generated at:** [ISO-8601 timestamp]

## Description

[5–6 sentences max. State the outcome and the direct reason — what failed, where (cite transcript entries as `entry N`), and what the evidence says. No background, no fixes.]

## Transcript

**1. turn — User**

```text
[PII-redacted user message text, verbatim.]
```

**2. turn — Assistant**

```text
[PII-redacted assistant prose reply, verbatim.]
```

**3. [skill | tool] — `[name]` — status: [ok | error | unknown]**

- **Input:** [one-line summary]
- **Output:**

  ```text
  [result, truncated to ~2000 chars; `_No output._` if none. Failure message goes here.]
  ```

[...continue numbering chronologically; turns and tool calls interleave...]
````

### 6. Confirm to the user

After writing, print: the absolute file path, the outcome, and the count of transcript entries. Do not echo the full report back.

## Examples

- **Non-watsonx.data integration session.** Refactoring an unrelated Go service → one-line skip, no file written.
- **Successful session (manual invocation).** The agent built a pyflow, submitted it, the run polled green; the user files a bug report for the record → Outcome `success`.
- **Failed session (proposed → accepted).** The agent repeatedly guessed stage / connector configuration instead of consulting the relevant lookup tool, the flow failed to compile, the agent proposes the report and the user accepts → Outcome `failure`, Description cites the missed lookup.