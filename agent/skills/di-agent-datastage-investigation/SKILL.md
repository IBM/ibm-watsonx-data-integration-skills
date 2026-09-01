---
name: di-agent-datastage-investigation
description: "Deep investigation of a failed run of a DataStage job already in operation — a scheduled or production job, or any job whose failure the user asks you to investigate. Works end-to-end from MCP tools: logs, job config, flow structure, connection health. Produces a root-cause diagnosis, not a fix. NOT for a run that failed while a flow was being built or edited — those are handled by the di-agent-flow-lifecycle skill, which runs its own investigation and loads this one only when a production-depth analysis is needed."
---

# DataStage Job Investigation

Use the MCP tools available through the `de-mcp` server to investigate job-run failures.
You are given: a **job** (its name or UUID), a **run ID** (UUID, optional), and a **project ID** (UUID).

---

## Step 1 — Resolve the Job ID (only if given a name)

If you have a job name but not its UUID, resolve it first:

```
list_jobs(project_id=<PROJECT_ID>)
```

Match `job_name` in the response to get the `job_id`. The response shape is:
```json
{
  "jobs": [
    {"job_name": "...", "job_id": "...", "job_link": "...", "job_type": "..."}
  ],
  "next": null
}
```

---

## Step 2 — SCOPE: Gather Context

### 2a. Identify the Run to Investigate

If no `run_id` was provided, list recent runs to find the one to investigate:

```
list_job_runs(
    project_id=<PROJECT_ID>,
    job_ids=[<JOB_ID>],
    selection_strategy="latest",
    limit=20
)
```

**Response shape notes** (from live observation):
- The top-level `"job_runs"` value is a **list of lists** — one inner list per `job_id`. With one job ID:
  `result["job_runs"][0]` is the list of run entries.
- Each entry: `job_run_id`, `job_id`, `job_name`, `job_run_status`, `duration`, `created_at`,
  `last_modified_on` (epoch ms as a string, not ISO-8601), `job_run_link`.
- **`job_run_status`** uses raw API casing: `"Failed"`, `"Completed"`, `"CompletedWithWarnings"`,
  `"CompletedWithErrors"`, `"Canceled"`, `"Canceling"`, `"Running"`, `"Starting"`.
- **`duration`** is `null` while a run is in-progress, and `0` for a legitimately zero-second
  completion. Check `job_run_status` alongside `duration` to distinguish the two.

Pick the most recent `"Failed"` run (or the run_id the user specified) as `<RUN_ID>`.

Look for patterns across multiple runs: consistent failures vs. intermittent; failures only
after a certain date (something changed — data, schema, config, environment, connection).

### 2b. Get Full Run Details

With the `job_id` and `run_id` in hand, call the primary diagnostic tool:

```
get_job_run_details(
    project_id=<PROJECT_ID>,
    job_id=<JOB_ID>,
    run_id=<RUN_ID>
)
```

Parse the response for:

- **`job_run_status`** — `"Failed"`, `"Completed"`, `"CompletedWithWarnings"`, etc.
- **`duration`** — seconds; `0` with `"Failed"` status means the job started but completed
  instantly (likely a pre-execution error).
- **`errors[]`** — entries from `status_reason.errors`. Each has:
  - `"code"` — e.g. `"##EIIS-DSEE-TFOR-00089"` (strip leading `##E`/`##W` to get the bare code)
  - `"message"` — human-readable description
  - `"description"` — stage location, e.g. `"error at <Generic_1,0>"`
  This is often enough to identify root cause without needing logs.
- **`stage_metrics[]`** — per-stage `rows_read`, `rows_written`, `state`, `stage_name`,
  `stage_type`. Find the first stage whose `state` is `"failed"` — that is the failure point.
- **`link_metrics[]`** — per-link `rows_read`, `rows_written`, `source`, `dest`. Use to trace
  where data stopped flowing.
- **`flow_limits`** — `{"row_limit": int, "warn_limit": int}`. If `warn_limit` is low (e.g. 100)
  and warnings were generated, the job may have failed due to exceeding the warning threshold.
- **`job_parameters[]`** — combined list of `{"name": str, "value": str}` pairs sourced from
  `entity.job_run.job_parameters`. This is the authoritative list — do **not** read
  `configuration.env_variables` or `configuration.job_parameters`, which are incomplete flat
  strings. Entries whose `name` starts with `$` are environment variables (e.g.
  `$APT_WLM_PARTITION_COUNT`, `$REMOTE_ENGINE`); all others are job parameters (e.g.
  `NUM_PARTITIONS`, `HARDWARE_SPECIFICATION`). Check both groups for misconfigured or missing
  values.
- **`total_rows_read` / `total_rows_written`** — aggregate row counts; a large discrepancy
  suggests potential job logic issues.

### 2c. Inspect Flow Structure (if stage-level errors need context)

If an error names a specific stage and you need to understand its configuration:

```
retrieve_datastage_flow_code(
    project_id=<PROJECT_ID>,
    flow_name=<FLOW_NAME>
)
```

> **Note:** The flow name is the job name **without** the trailing ` .DataStage job` suffix.
> e.g. `"db2_to_snowflake.DataStage job"` → use `"db2_to_snowflake"`.

Use to understand:
- Stage wiring and data flow topology
- Stage configurations (partition keys, sort keys, connector settings)
- Column mappings and transformer expressions
- Connections used in the flow

### 2d. Inspect Connection Details (if errors point to connection/schema issues)

List connections in the project:

```
list_connections(project_id=<PROJECT_ID>)
```

Inspect the specific connection:

```
inspect_project_asset(
    project_id=<PROJECT_ID>,
    asset_ids=[<CONNECTION_ID>],
    asset_type="connection"
)
```

Check: host, port, database name, username, datasource type. Compare against what the failing
stage is configured to use. Look for stale credentials, wrong endpoint, or database name drift.

> **Gap:** No MCP tool can actively test connection reachability (`validate-connection`).
> If reachability is in question, ask the user to validate manually in the UI.

### 2e. Inspect Data Assets / Table Definitions (if schema mismatch is suspected)

List data assets:

```
list_data_assets(project_id=<PROJECT_ID>)
```

Inspect a specific asset:

```
inspect_project_asset(
    project_id=<PROJECT_ID>,
    asset_ids=[<ASSET_ID>],
    asset_type="data_asset"
)
```

Preview live rows from a connected table or file-based asset:

```
read_data_preview(
    project_id=<PROJECT_ID>,
    binding="<connection_id>:/<SCHEMA>/<TABLE>"
)
```

For file-based assets stored directly on the platform:

```
read_data_preview(
    project_id=<PROJECT_ID>,
    binding="<ASSET_ID>"
)
```

Use these to compare expected vs. actual schema — column names, types, nullability, ordering.

---

## Step 3 — Compare most recent successful run with the failed run

- Use `list_job_runs` as in Step 2a to get the most recent Completed or CompletedWithWarnings run.
- If there is no successful run then there is most likely a configuration or logic issue with the job just skip to Step 4.
- If there is a recent successful run use `get_job_run_details` as in Step 2b to get the successful run metadata.
- Compare the successful run metadata with the failed run metadata.
   - Check for differences in `job_parameters` (both the env var entries with `$` prefix and the plain
     job parameter entries) which could have triggered a problem.
   - Compare stage_metrics to see if rows_written, rows_read, total_memory, or stage_seconds_cpu
     are significantly different. The expectation being that these values are the same or lower in
     the failed case since the job did not complete.

---

## Step 4 — LOGS: Analyze Logs

- If `get_job_run_details` errors are not sufficient for a root-cause determination, fetch the full log:
```
get_job_run_logs(
    project_id=<PROJECT_ID>,
    job_id=<JOB_ID>,
    run_id=<RUN_ID>,
    grep="##[EF]"
)
```

- Start with `grep="##[EF]"` (errors and fatals only). Before issuing a second call,
  check `message_id_counts` in the response
  — if a severity bucket is empty there are no messages of that type and you do not need another call.
    Widen to `grep="##[EWF]"` only if the error output is sparse or inconclusive.
- If grep="##[EF]" returns no lines and message_id_counts shows zero errors,
  retry with structured_only=False to see parameter dumps and pre-execution output.

Look for:
- Lines with `ERROR`, `Fatal Error`, `FAILED`
- Stage names in angle brackets: `<stage_name,0>`
- Exception classes: `SCAPIException`, `RuntimeException`, `OutOfMemoryError`
- SQL errors: `SQL compilation error`, `ORA-*`, `SQLCODE`

**Error code classification** — the prefix identifies which component failed:

| Prefix | Component | Action |
|--------|-----------|--------|
| `CDICO*` | Connector stage | Check connector config, data format, target health |
| `IIS-DSEE-TBLD-*` | Parallel engine build/compile | Check flow definition, stage compatibility |
| `IIS-DSEE-TFOR-*` | Operator runtime | Check stage configuration, partitioning |
| `IIS-DSEE-TFCC-*` | Character conversion | Check codepage/encoding settings |
| `IIS-DSEE-TFPM-*` | Process manager | Check resource limits, node configuration |
| `IIS-DSEE-TFRS-*` | Record/schema | Check field lengths, delimiters, schema |
| `IIS-DSTAGE-RUN-*` | Runtime/debugger | Check network, TCP, debugger settings |
| `NDS-DSEE-*` | Engine-level | Check engine health, service status |

**Dynamic apt config file variation** - scheduling differences can cause intermittent failures

Jobs running with multiple partitions can sometimes have undesirable behavior when more than one
of the partitions are placed on the same pod. The pods the job ran on can be determined from the log
entry with the id IIS-DSEE-TFSC-00022. In this log there will be one or more fastname values which
indicate the pod that each partition of the job ran on. Compare these values for the failed run
with values from a successful run.

---

## Step 5 — RESEARCH: Unfamiliar Error Codes

When you encounter an unfamiliar error code or message, consult in this order:

1. **`di-agent-knowledge-engine-datastage` skill** — engine internals, stage semantics,
   partitioning, APT config, and per-stage error patterns.

2. **`datastage_property_lookup` MCP tool** — accepted property names and values for the
   stage that produced the error:

   ```
   datastage_property_lookup(
       requests=[{"stage": "<stage_type>"}]
   )
   ```

3. **IBM documentation** (use `websearch` / `webfetch` if available):
   - `IBM DataStage error <ERROR_CODE>`
   - `IBM Cloud Pak for Data DataStage troubleshooting <error message>`
   - Troubleshooting reference: `https://dataplatform.cloud.ibm.com/docs/content/dstage/dsnav/topics/troubleshooting.html`

---

## Common Failure Patterns

| Pattern | Key Symptom | Next Step |
|---------|-------------|------------|
| Server error on start | `NDS-DSEE-TDSR-0000E`, `duration=0` | Check engine health; look for other concurrent failures |
| Compilation timeout | Transformer stage hangs, `duration=0` | Check `APT_COMPILEOPT` in `get_job_run_details` `job_parameters` |
| Resource exhaustion | OOM, exit code 137, SIGKILL in errors | Check `job_parameters` in `get_job_run_details` for memory/CPU config |
| Warning limit reached | `warn_limit` exceeded | Check `flow_limits.warn_limit` in `get_job_run_details`; look at `stage_metrics` for warning counts |
| Connection failure | Timeout, auth error | `list_connections` → `inspect_project_asset` → validate manually (gap) |
| Schema mismatch | `Object does not exist`, type errors | `inspect_project_asset` data_asset + `read_data_preview` |
| Delimiter/encoding | `CDICO9999E`, `TFCC` errors | Check stage config in `retrieve_datastage_flow_code` vs. source format |
| Abnormal termination | `SIGKILL` / `TFPM-00339` in errors | Check resource limits; `get_job_run_details` `job_parameters` for `HARDWARE_SPECIFICATION` |

---

## Output Diagnosis - After completing the steps above, produce a root-cause diagnosis. **Do not produce a fix.**

Structure the diagnosis as:
- **Error:** The exact error code(s) from `get_job_run_details` `errors[]` or the log.
- **Stage:** Which stage failed (from `errors[].description` or `stage_metrics`).
- **Cause:** Why it happened — cite the specific `get_job_run_details` field, log line, or config value
  that confirms it.
- **Evidence:** Which MCP tool call returned the confirming data.
- **Gaps:** Any investigation steps that could not be completed due to missing MCP coverage.

If the investigation is inconclusive after all phases, state clearly what could not be determined
and which gap(s) are responsible. Do not guess.

---

## Post Diagnosis - After providing a diagnosis to the user check if there are any follup tasks that may make sense.

- If the investigation involved a job failure
  - Use `get_job_alert_definitions` to check if any alert definitions are configured for this job:
```
get_job_alert_definitions(
    project_id=<PROJECT_ID>,
    job_name=<JOB_NAME>
)
```
    - If `total == 0` (no definitions), ask the user if they would like to create one for job failures.
      If yes, call `create_alert_definition` with `alert_type="JobRunState"` and
      `condition="this.state == 'failed'"`.
    - If definitions exist, find any triggered alert for this job using `list_alerts`:
```
list_alerts(
    project_id=<PROJECT_ID>,
    status=["TRIGGERED"],
    alert_type=["JobRunState"]
)
```
    - Match the alert to the run by comparing run_reference.run_uid against the known <RUN_ID>,
      and to note that job_reference fields may be null and are unreliable for matching.
      - If an alert is found and the status is `"TRIGGERED"`, ask the user if they would like to
        acknowledge or resolve it. If yes, call:
```
update_alert(
    alert_id=<id>,
    project_id=<PROJECT_ID>,
    status="ACKNOWLEDGED"   # or "RESOLVED" depending on user preference
)
```
