# DIAGNOSE state

## Entry

A run failed, or completed but returned wrong / empty output.

This state produces a **root-cause class**, not a fix. Naming the class is what decides where you go next — that decision is the whole reason this state exists.

## Step 1 — Get a diagnosis

**A run that failed while you were building the flow is diagnosed here, inline.** That is the case this state exists for: the flow is minutes old, it has usually never succeeded, and the likely causes are the ones authoring introduces — a guessed column, a type mismatch, a binding that points somewhere else. Work the steps below.

**Load `di-agent-datastage-investigation` instead when the failure is not yours** — a scheduled or production job, a run someone else's flow produced, or any case where the user asks you to investigate a job rather than fix the flow you are building. It owns the deep observability procedure for flows already in production. If it is not in your catalog, the steps below are self-sufficient for the case this state is for; carry on without it.

> **If you do load it, you come back here.** It produces a root-cause diagnosis and deliberately stops there — it does not decide what to do next. Bring its diagnosis to Step 2, classify it, and route on the class. Handing off never ends the lifecycle.

The inline investigation:

1. `list_job_runs(project_id=…, job_ids=[<job_id>], selection_strategy="latest", limit=20)` — find the failed run, and note whether failures are consistent or intermittent, and whether they start after a particular date.
2. `get_job_run_details(project_id=…, job_id=…, run_id=…)` — its `errors[]`, `stage_metrics[]` (the first stage with `state: "failed"` is the failure point), and `job_parameters[]` are usually enough on their own. `Completed` and `CompletedWithWarnings` are both successes: if you see either, the run worked — report it and stop.
3. `get_job_run_logs(project_id=…, job_id=…, run_id=…, grep="##[EF]")` — errors and fatals first. Check `message_id_counts` before widening to `##[EWF]`; if there are zero errors, retry with `structured_only=False`.
4. Unfamiliar error code → `di-agent-knowledge-engine-datastage`, then `datastage_property_lookup` for the stage that produced it.

Error-code prefixes tell you which component failed: `CDICO*` connector, `IIS-DSEE-TBLD-*` build/compile, `IIS-DSEE-TFOR-*` operator runtime, `IIS-DSEE-TFPM-*` process manager (resource limits), `IIS-DSEE-TFRS-*` record/schema, `NDS-DSEE-*` engine-level.

## Step 2 — Classify into exactly one root-cause class

| Class | Looks like | The flow is… |
|---|---|---|
| **transient / environmental** | timeout, pod/scheduling variation, connection blip, engine health, auth expiry, resource exhaustion (OOM, SIGKILL) | not at fault |
| **deterministic flow bug** | bad expression, schema/type mismatch, missing column, wrong stage config, empty output from a wrong join or filter | wrong and must change |
| **broke a previously-working flow** | this flow ran successfully before a recent edit | regressed by the last change |

The clearest signal for the first two: did this same flow ever run successfully with the same inputs? If yes and nothing changed in the flow, suspect environmental. If it has never succeeded, suspect the flow.

### Read the mechanism, not the stage name

**A runtime error names the stage it surfaced in. That is the location, not the cause.** The engine reports the stage that was executing when the run died, so an infrastructure failure — a dropped connection, an evicted node — is reported against whichever stage happened to be running. Classifying on the stage name is the most common misdiagnosis here, because it turns every environmental failure into an apparent flow bug.

Read past the stage to the **mechanism** — what the message says actually went wrong:

- *timed out, lost connection, connection reset, node unreachable, killed, out of memory, terminated before any rows were written* → **transient**. The flow never got the chance to be wrong.
- *cannot convert, column not found, type mismatch, invalid expression, unexpected null, wrong cardinality* → **deterministic**. The flow asked for something impossible.

A message that names a stage *and* describes a timeout is a timeout. Opening that stage's code to inspect it is wasted work, and it tends to end in editing a flow that was never broken.

### State the class, then act on it

Say the class and the evidence in one line before your next tool call — "the run hit a socket timeout, so this is a network problem rather than anything wrong with the flow; re-running it." Then follow it. Re-reading the same log does not produce new evidence; a second run that fails the same way, or a tool result that contradicts the verdict, does.

**One retry for a suspected transient.** If the second run fails identically, it was not transient — re-diagnose rather than retrying a third time.

## Step 3 — Route on the class

- **transient / environmental → RUN.** Retry the run — `create_job_run` on the existing job, nothing else. **Do not edit, recreate, or delete the flow, and do not retrieve its code**: you have just concluded the flow is not at fault, so there is nothing to find in it. Recreating a flow after a timeout is the second-largest source of duplicate flows.
- **deterministic flow bug → AUTHOR** (EDIT path). Fix in place — `update_datastage_flow`, or `create_pyflow(replace_flow_id=…)` — on the same flow id.
- **broke a working flow → RECOVER.** Restore the last known-good version; RECOVER explains how.

**"Deterministic flow bug" and "broke a working flow" look identical in the error — the same broken derivation or bad column. The deciding question is whether this flow ever worked.** If it never had a successful run, it is a plain bug: there is no good version to go back to, so fix it forward (AUTHOR). If it *did* work before and broke after a change — a prior `Completed` run, a pre-edit snapshot exists, or the user says "it worked yesterday" — it is a **regression**, and the right move is to put the known-good version back, not to re-derive a fix by hand.

Restoring is not the destructive dance it sounds like: it is an in-place overwrite of the broken flow with the good version's definition (`retrieve_datastage_flow_code` on the snapshot → `update_datastage_flow` on the flow), keeping the id and jobs — see RECOVER. **Hand-fixing a regression is a gamble: you are trying to reconstruct behaviour you already have saved.** Prefer the saved version. Only fall back to a forward fix if no good version can be found.

## When you stop, say that the run failed

**A flow that has never run successfully is never reported as finished.** This is the single most damaging failure in this state, and it is a *reporting* failure, not a routing one: after several failed runs and repair attempts the flow does exist, so the reply drifts to "the flow has been created — would you like me to run it?" The user is left believing they have a working flow and a pending step, when what they have is a flow that has failed every time it ran.

Whenever you leave this state without a successful run, the reply must carry three things:

1. **That the run was attempted and failed** — with how many times, if more than once. Never present an attempt you already made as something still to try.
2. **What you concluded**, in the user's terms — the root-cause class and the evidence for it.
3. **What you changed, and what is still wrong.** If repairs did not fix it, say that plainly: *"I couldn't get this to run; here is what is failing and what I'd need to resolve it."*

Do not offer to run a flow you have already run. If the user asks you to run it again after this, run it — but if it fails the same way, say so again rather than returning the same "created successfully" answer a second time.

**Cap the repair loop.** Re-authoring the flow after a failed run is bounded: at most **two** repair attempts on the same root cause. If the third run fails, stop and report — you are no longer converging, and further `create_pyflow` / `update_datastage_flow` calls just churn the asset and its snapshots. A repair that does not change the error is evidence the diagnosis was wrong, not a reason to repair again.

## If the diagnosis is inconclusive

Report what you found and what you could not determine, and ask the user. **Do not guess by recreating the flow.** If the evidence points at a product defect rather than the user's flow, offer `di-agent-bug-report`.

## Follow-up

After delivering a diagnosis for a job failure, if alert tooling is available, check whether the job has alert definitions (`list_alert_definitions(project_id=…, job_name=…)` — it takes the job's *name*, not its id) and offer to create one for failures. If a TRIGGERED alert matches this run, offer to acknowledge or resolve it.
