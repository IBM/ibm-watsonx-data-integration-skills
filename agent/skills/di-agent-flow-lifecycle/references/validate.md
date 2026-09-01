# VALIDATE state

## Entry

A flow exists, but "known-runnable" is not yet established. This is the convergence point where both authoring paths become equal: however the flow was made, it leaves here compiled or it does not leave here.

## Step 1 — Was the flow already compiled by the tool that made it?

Check the authoring backend's **Validation** row in `registry.md`. Both backends compile as part of authoring, so in the normal case **there is nothing left to do here**:

- **`pre_publish` (pyflow)** — `create_pyflow` compiles and IR-validates the DSL before publishing, then compiles the published flow on the engine. A result **without** `status: "compile_error"` means both gates passed: compiled and ready to run.
- **`on_save` (datastage-sdk)** — `create_datastage_flow` / `update_datastage_flow` compile the flow as part of the call. Same signal: no `status: "compile_error"` means it compiled.

If the authoring call succeeded, exit to RUN. Do not call anything extra to "check" the flow — there is no standalone compile tool, and creating a job just to test compilation is wasteful.

## Step 2 — Handle a compile error

A compile failure comes back from the authoring call itself, shaped like this:

```
status:         "compile_error"
flow_id:        "<the flow — it IS saved>"
flow_link:      "<opens it in the UI>"
compile_errors: [ { stage, link, reason }, … ]   # `link` is the DataStage link's NAME, not a URL.
                                                 # Falls back to `compile_error`, a plain string,
                                                 # when the engine's payload wasn't structured.
```

**If the result carries a `flow_id`, the flow exists** — it was saved and then failed to compile; it was not rolled back. (A malformed-DSL failure raises instead and produces no `flow_id`; there is nothing saved and nothing to fix in place — rewrite the DSL and call `create_pyflow` again.) So whenever you have a `flow_id`:

- Transition to **AUTHOR**, EDIT path. Fix with `update_datastage_flow` on that **same** `flow_id` (or `create_pyflow(replace_flow_id=…)` for a pyflow flow).
- **Do not create a new flow.** **Do not delete the broken one.** The id is what you edit against, and deleting it strands anything already pointing at it.
- Come back through here after the fix.

### Fix the error you were given

`compile_errors` names the **stage** and the **reason**, so the fix can be equally specific. Regenerating a broadly-similar flow and resubmitting is not a fix — it usually reproduces the same error, having spent a full submission.

Before resubmitting, know which stage and property failed, and what you are changing so that *that* reason no longer holds. Say it in one line as you submit: "the Join stage was given `join_keys`, which it doesn't accept; switching to the `key` property it does." That is also how you can tell next time round whether the fix worked.

**The same error twice means the fix was wrong** — look the property up (`datastage_property_lookup`, `recommend_datastage_stages`) rather than submitting a third variation. One lookup ends a spiral that trial-and-error will not. If it is still unclear after that, tell the user the specific blocking error instead of continuing to resubmit.

## Step 3 — The backstop at job creation

`create_job` still refuses an uncompiled or invalid flow, returning the same `status: "compile_error"` shape with the same `compile_errors` list. That is a backstop for flows that were changed outside this lifecycle, not the primary gate. If you hit it, the response is identical: fix in place on the same `flow_id`, never recreate.

## StreamSets notes

A StreamSets flow cannot run without an environment attached. If `create_pyflow` was called without `environment_id`, call `set_streamsets_flow_environment` (pick one from `get_streamsets_environments`) before running. This is part of "known-runnable" too.

StreamSets validates *before* publishing, so its failure is a different shape: `status: "validation_failed"` with `validation_issues` and **no `flow_id`** — nothing was saved. Fix the DSL from the issues listed and call `create_pyflow` again; there is no flow to edit in place, and `replace_flow_id` would target the wrong thing. If an issue is a missing configuration value only the user has, ask for it rather than guessing.

## Exit → RUN

The flow is compiled. RUN creates the job and runs it. On a compile error, exit to AUTHOR instead — never onward to RUN.
