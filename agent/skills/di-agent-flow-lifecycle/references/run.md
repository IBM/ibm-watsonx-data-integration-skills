# RUN state

## Entry

The flow is known-compiled (VALIDATE passed) and the user wants results. Flow job runs are different from "pipelines", which are higher-level orchestration pipelines that are not supported.

## Steps

1. **Get a job for the flow — just call `create_job`.**
   - `create_job(flow_id=…, project_id=…, engine=…)` looks the flow's jobs up for itself (`get_asset_relationships` → `used_by`, scoped to this flow) and **returns the existing job** with `reused_existing_job: True` when there is one, instead of minting a second. So you do not pre-check, and you do not list every job in the project to find out.
   - Read `reused_existing_job` in the result: `True` means the job was already there, and a run of it may already exist — see the in-flight check below before starting another.
   - `create_job` also refuses an uncompiled or invalid flow, returning `status: "compile_error"` with a `compile_errors` list. If you see that, go to **AUTHOR**: fix with `update_datastage_flow` on the same `flow_id`. Never recreate the flow.
   - A flow gets one job: its name is derived from the flow's name plus a project-level suffix, so a second `create_job` for the same flow cannot produce a differently-named job anyway. Deliberate second jobs are a DataStage UI operation.
2. **`create_job_run(job_ids=[<job_id>], project_id=…)`.** Pass `runtime_parameters` if the flow uses parameter sets — load `di-agent-parameter-sets` when it does.
3. **Poll until terminal.** `poll_datastage_job` for DataStage; `get_streamsets_job_status` for StreamSets.
4. **On success, read the output.**
   - `q.output()` file assets → find the asset with `list_data_assets(project_id=…, entity_name=<target_path>)`, then `read_data_preview(project_id=…, binding=<asset_id>)`. The real filename is `target_info[].target_path` from the `create_pyflow` result, not the `name` passed to `q.output()` — the compiler prefixes and suffixes it.
   - `q.write()` destinations → `read_data_preview(project_id=…, binding="<connection_id>:<path>")` on the target connection.

If a run is already in flight against this job, do not start a second one — poll the existing run.

## The output does not exist until *this* run has finished

Steps 1–3 are what cause the output to exist. **A flow's output asset is created by a completed run of its current definition** — so after authoring or fixing a flow there is nothing to read until you have run it again. A previous run's output came from the old definition: stale at best, usually absent.

So when an output lookup comes back empty, check *whether the run happened* before questioning the name:

- Was there a `create_job_run` polled to a terminal success **after** the most recent edit? If not, that is the answer — run it, then look.
- Did the run succeed? A failed run writes no output → DIAGNOSE.
- Only once a successful run is confirmed is the name in question, and then re-read `target_path` from the authoring result rather than guessing variants.

## Exit

- **Terminal success** → done. Surface the `flow_link` / `job_link` and the results to the user.
- **Failure, or empty / wrong output** → transition to **DIAGNOSE**.

**Whatever the outcome, the run is part of what you report.** You ran the flow, so the user is told how that went — a success with its results, or a failure with what failed. Never close on "the flow was created" alone once a run has been attempted, and never offer to run a flow you have already run. DIAGNOSE carries the full rule for what a failed-run reply must contain.

Do not edit, recreate, or delete the flow before a diagnosis says the flow is at fault. A failed run is not evidence that the flow is wrong — most first failures are environmental. Retrying blind is also wrong; go through DIAGNOSE, which decides whether a retry is the right move.
