# Flow Execution Reference

Use this file only after generating the full-pushdown SDK script or MCP `sdk_code`
subset and only when the user asks to create, run, monitor, or fetch results.

## Preferred Execution Order

For **build pushdown DataStage flow and run**:

1. Generate and save the complete SDK script.
2. Build the no-boilerplate MCP `sdk_code` subset from the fill block.
3. If `create_datastage_flow` is available, call it first to publish a new flow.
   If it errors because the flow name already exists, do NOT retry automatically —
   ask the user whether to overwrite it with `update_datastage_flow` or use a new
   name. Use `update_datastage_flow` directly only when revising a flow you know
   already exists.
4. If create/update succeeds, use MCP job tools when available:
   `create_job`, `create_job_run`, `poll_datastage_job`.
5. **Fetch outputs only when the sink produced a data asset.** This step
   is sink-dependent:
   - **Sequential file** sink → fetch with the result tool
     (e.g. `get_flow_results_from_cos`). This is the only sink that
     persists rows as a data asset the agent can read back.
   - **PxCopy** sink (target pushdown only) → **skip this step**. PxCopy
     is pure pass-through; no file is written. The job's success status
     from step 4 is the only observable, which is exactly the point —
     the real work happened inside the source database via before-SQL,
     and the user has already opted out of writing observability rows
     anywhere.
   - **PxPeek** sink → **skip the result-fetch tool**. PxPeek writes to
     the job log, not to a data asset. If the user asked to see the
     observability output, return the relevant portion of the job log
     from `poll_datastage_job` (or a log-fetch tool when available)
     instead of calling a result tool.
6. If MCP create/update fails after actionable SDK-code corrections, or job/result
   tools are unavailable, run the generated script locally as-is:
   `python <generated_script>.py --create_flow`, then
   `python <generated_script>.py --run_flow --monitor_job`.

The skeleton's no-flags invocation is acceptable for local fallback because it defaults
to create + run + monitor. If only monitoring remains, run
`python <generated_script>.py --monitor_job`.

## Local Credential Preparation

Before local script execution, prepare the script directory:

1. Use the generated script's parent directory as the save directory.
2. Create or update `credentials.env` only when it is missing or incomplete.
3. Populate it from available environment values without printing secrets:
   - `API_KEY` or `WATSONX_API_KEY`
   - `BEARER_TOKEN` or `DE_MCP_BEARER_TOKEN`
   - `BASE_AUTH_URL` or `IAM_URL`
   - `BASE_API_URL` or `GATEWAY_URL`
   - `PROJECT_ID` or `WATSONX_PROJECT_ID`
4. Prefer preserving existing values already present in `credentials.env`.
5. Set restrictive permissions when possible, e.g. `chmod 600 credentials.env`.
6. Never echo, log, or include credential values in the response. Do not commit
   `credentials.env`.
7. If required values are unavailable, ask only for the missing runtime values.

## Command Selection

- **Create the flow**: call `create_datastage_flow` with the MCP subset to publish a
  new flow; if the name already exists it errors — ask the user before overwriting
  with `update_datastage_flow` or renaming. Use `update_datastage_flow` directly to
  revise a flow you know exists. If creation fails after actionable corrections, run
  `python <generated_script>.py --create_flow`.
- **Run the flow / run a job**: prefer MCP job tools for the flow created by
  `create_datastage_flow`. If unavailable or failing, run
  `python <generated_script>.py --run_flow --monitor_job`.
- **Full lifecycle**: try `create_datastage_flow`, then MCP job tools, then
  result tools. Use the script with no flags only as local fallback.
- **Monitor a running flow**: run `python <generated_script>.py --monitor_job`.

Honor script parameters such as `--flow_name` or `--poll_interval` when present.
