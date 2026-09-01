---
name: di-agent-flow-lifecycle
description: "Entry point for ALL flow work in watsonx.data integration — creating, editing, running, diagnosing a failed run, or backing up/restoring a flow. Load this FIRST whenever a request touches a data flow. It gathers intent — including which engine the flow runs on — routes to exactly one lifecycle state, and applies a fixed precedence order so routing is consistent run to run."
---

# Flow Lifecycle State Machine

Flow work runs as a **state machine**. Every request enters exactly one **state** — AUTHOR, VALIDATE, RUN, DIAGNOSE, or RECOVER — and each state's rules live in a **separate reference file under `references/`**. Those files are not in your context: the catalog lists them by name, and a name is not its contents. **Entering a state means loading its reference file yourself and following it** — reading this file does not pull it in. Until you load it you are guessing, and the states exist because the intuitive guess (duplicate the flow instead of editing it, restore the newest snapshot, "fix" a flow that only timed out, delete snapshots to tidy up) is reliably wrong.

This skill owns **routing only**. Depth lives elsewhere: authoring backends are their own skills (`di-agent-flow-pyflow`, `di-agent-flow-datastage`), stage/property knowledge is in `di-agent-knowledge-engine-datastage` / `-streamsets`, and the state playbooks are the reference files here.

**This vocabulary is internal — never say it to the user.** States, backends, the registry, "pyflow", "the DSL", "the SDK", precedence rules, and this skill's own name are how *you* decide, not how you describe what you did. The user sees flows, stages, jobs, runs, and files. "I can't build the flow that way, but I can build the same thing the supported way" is right; "pyflow can't express that, so I'm escalating to the datastage-sdk backend" is the same fact leaked as jargon. Do not paste DSL or SDK code into a reply either — show it only when the user asks to see code.

## Step 1 — Gather intent + current state

Before choosing anything, establish these four things. They are cheap, and every routing rule below depends on them.

- **Target flow?** Is there an existing flow this request refers to — an id already in context, or one found via `list_datastage_flows`? This is the create-vs-edit input.
- **Job running?** Is a run in progress against that flow (`list_job_runs`)? Guard destructive edits; ask before overwriting a flow that is mid-run.
- **Engine.** `datastage` or `streamsets`.
- **Goal.** *What the user is trying to achieve* — not a list of stages. pyflow works from the goal; you do not need stage-level expertise to start.

If the request is read-only (list, preview, retrieve, "what does this flow do"), it is **not** a state. Call the tool and answer.
If the request is related to pipelines, report to the user that pipelines are unsupported and do not enter the flow lifecycle. Flow job & runs are different from "pipelines", which are higher-level orchestration pipelines that can contain flow job runs as nodes along with other control logic.

## Step 2 — Classify into exactly ONE state, then load its file

| If the intent is… | State | Load |
|---|---|---|
| make or change a flow's structure/content | **AUTHOR** | `references/author.md` |
| make an existing flow runnable / confirm it compiles | **VALIDATE** | `references/validate.md` |
| execute a flow and get results | **RUN** | `references/run.md` |
| understand why a run failed or gave wrong output | **DIAGNOSE** | `references/diagnose.md` |
| back up, restore, or de-duplicate flows | **RECOVER** | `references/recover.md` |

Pick the state that matches the *first* thing you must do. "Fix this flow and run it" enters at AUTHOR and reaches RUN through the legal transitions below — it is not two independent requests.

Load that state's file **before** Step 3 and before any tool that creates, edits, runs, deletes, or restores a flow — you have not entered the state until its file is in your context. Each legal transition into a new state is another load: one per state you enter.

## Step 3 — Precedence order (applies to every decision inside a state)

When more than one rule bears on a choice, the **lower number wins**.

1. **Explicit user instruction** — a named backend, a named stage, "use the SDK". ← highest
   *Only for something that exists.* If the user names a backend or path that is not in `references/registry.md`, this rule cannot be satisfied, and falling back to the default without saying so is a silent substitution. Say which part you could not do, then do the rest the normal way — `author.md`, "Call out what you cannot do, then do your best on the rest".
2. **Expressiveness** — can the default backend (pyflow) express this at all? If not, escalate.
3. **What already exists** — a flow already exists → this is an EDIT, never a new create. A job is running → guard before changing anything.
4. **Reliability / cost** — prefer the validated, cheaper, round-trippable path.
5. **Default: pyflow.** ← lowest

Worked example: *"add a running-total column to the orders flow."* A flow exists (rule 3) → this is an EDIT; do **not** create a second flow. Whether you re-emit it in pyflow or splice its existing code turns on whether you authored it in pyflow this session — `author.md` Step 1 decides that.

**Bias toward pyflow is about CREATE, not about overwriting existing flows.** Rule 5 says start a *new* flow in pyflow; it never says re-express one that already exists. Editing works on the definition the flow already has.

## Step 4 — Say what you decided, and why

Each state turns evidence into one decision: which backend, which root-cause class, which snapshot. **State that decision and the evidence behind it in one line, in the message you send the user.** The user cannot see your reasoning, and these calls have consequences they are entitled to understand — a capability limit that changed how their flow was built, a diagnosis that means the flow was never at fault, a restore that discards work.

Put it in your **final** message. That is the one the user reads; there is no slot for narration between tool calls, and a decision mentioned earlier but dropped from the summary was not communicated. Say it **even when the work went perfectly** — a clean run is the most common reason this gets skipped, and the user still needs to know why their flow was built the way it was.

| State | What the reply must state |
|---|---|
| **AUTHOR** | which backend, and — when it is not the default — what the request needs that pyflow cannot express. If any part of the request was something you could not do here, say that first, before describing what you built instead |
| **VALIDATE** | the specific error, and the change you made to fix it |
| **RUN** | the outcome — always — see below |
| **DIAGNOSE** | the root-cause class and the evidence that picked it |
| **RECOVER** | which snapshot, and why that one rather than the newest |

**Report what happened, not only what you decided.** A step that failed is reported as failed. **Never present a flow whose runs all failed as a finished flow, and never offer to run a flow you have already run.** "The flow was created — would you like me to run it?" after three failed runs is the worst reply this lifecycle can produce: every word of it is true and the whole of it is misleading. Say that it ran, that it failed, and what you found.

**Say the substance, not this vocabulary.** "The run failed on a network timeout rather than anything wrong with the flow, so I re-ran it" — not "classified transient per DIAGNOSE, routing to RUN".

## Legal transitions (do not invent others)

```
AUTHOR   → VALIDATE
VALIDATE → RUN | AUTHOR (compile error)
RUN      → exit | DIAGNOSE
DIAGNOSE → RUN (transient/environmental) | AUTHOR (deterministic flow bug) | RECOVER (broke a working flow)
RECOVER  → AUTHOR | RUN | exit
```

`exit` is not a state. It means the lifecycle is over: report and stop. There is no file to load.

The three DIAGNOSE outcomes above are **root-cause classes**, defined in `diagnose.md` Step 2. You classify into one of them there; this block only says where each one sends you.

Exhausted RECOVER and still stuck? That is the terminal escape: offer `di-agent-bug-report`.

## Four invariants the tools enforce (you cannot talk your way past them)

1. **A flow that exists is edited, never duplicated.** `create_pyflow(replace_flow_id=…)` overwrites in place and keeps the id; `update_datastage_flow` edits SDK flows in place. Calling `create_pyflow` *without* `replace_flow_id` to "redo" an existing flow mints a duplicate asset — the single largest source of flow clutter. Never delete-and-recreate to edit.

2. **A flow must compile before it runs.** Every authoring tool compiles the flow as part of the call, and `create_job` refuses an uncompiled flow as a backstop — both return the same `status: "compile_error"` with a per-stage `compile_errors` list. There is no separate "compile without running" tool, and none is needed. A flow that fails to compile is still **saved**: fix it in place on the same `flow_id`; never recreate it and never delete it.

3. **An in-place edit always leaves a rollback point.** Before overwriting, the editing tools snapshot the flow to `"{name}Backup{YYYYMMDDHHMMSS}"` and return `backup_flow_id` plus `backups` (the surviving history, oldest first). Up to 5 are kept and the **oldest is never discarded**. If the snapshot cannot be taken, the edit is refused and the flow is unchanged — so you never need `duplicate_asset` before editing.

4. **Version history cannot be deleted by accident.** `delete_asset` has two refusals, each overridable only after you have told the user what is at stake:

   - **`REFUSED_SNAPSHOT_DELETE`** — the target is a `"{name}Backup{timestamp}"` snapshot. "Clean up the duplicates" is the request that destroys version history: the copies a user wants gone are almost always these, and they are not copies the user made. Explain what they are; do not delete them to tidy up. Override: `deleting_a_snapshot_on_purpose=True`.
   - **`REFUSED_FLOW_HISTORY_DELETE`** — the target is a real flow that still has snapshots, and deleting it takes them with it. That is correct when removing the flow *is* what the user asked for, and destructive when it is a step inside a restore or repair — where it deletes the very version you were restoring from. **Restore by overwriting in place, never by deleting.** Override: `deleting_version_history_on_purpose=True`, and only when the user asked for the flow itself to be gone.

   Neither override is a confirmation step; do not set one to get past a refusal. Ordinary flow listings also hide snapshots while reporting how many (`hidden_snapshots`), so the count never looks like something being concealed.

## Backends

AUTHOR selects an authoring backend from `references/registry.md`. Two are registered, both stable: `pyflow` (both engines, the default) and `datastage-sdk` (DataStage only) — so on StreamSets pyflow is the only path. Nothing experimental is registered, so nothing else is selectable, whoever asks.

**Being unable to select it is only half the rule.** Build the flow the normal way by all means, but say that the path they named is not one of them. The user asked for something specific and cannot tell from a working flow that they did not get it. See `author.md`, "Call out what you cannot do, then do your best on the rest".

## Adjacent skills a state may send you to (not states themselves)

A state's file may tell you to load one of these; load it the same way you load a state file. Not every skill is enabled in every deployment — if one is not in your catalog, carry on without it rather than stopping or hunting for it.

- `di-agent-knowledge-engine-datastage` / `di-agent-knowledge-engine-streamsets` — stage and property reference; used by AUTHOR and DIAGNOSE.
- `di-agent-parameter-sets` — an orthogonal feature; load it when the flow uses parameter sets.
- `di-agent-bug-report` — the terminal escape after recovery is exhausted.
