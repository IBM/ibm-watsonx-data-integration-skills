---
name: di-agent-flow-datastage
description: "Reference for the verbose watsonx.data integration SDK for DataStage (batch) flows, with exhaustive stage and property access — the full engine stage catalog. Load this only after the di-agent-flow-lifecycle router has selected the datastage-sdk authoring backend — this is a syntax and stage reference, not a decision about whether to use it. If you have not routed yet, load di-agent-flow-lifecycle instead."
---

# Author and Edit DataStage Flows with the SDK

> **Routing lives elsewhere.** Whether a request should be authored here or in pyflow, and whether it is a create or an edit, is decided by the `di-agent-flow-lifecycle` skill (AUTHOR state). This file is the SDK reference and the mechanics of using it.

DataStage batch flows are written as SDK-style Python code and submitted via `update_datastage_flow` (edit an existing flow in place) or `create_datastage_flow` (create a new one). Auth, project context, and persistence are handled automatically.

The SDK reaches the **whole** engine stage catalog, including everything pyflow has no form for. That reach is also its cost: it needs exact stage types, property names, and enum values, which is why the router treats it as the escape hatch rather than the default.

**Both tools compile the flow as part of the call.** If it does not compile, the result comes back with `status: "compile_error"` plus `flow_id`, `flow_link`, and a per-stage `compile_errors` list — and the flow **is still saved**. Fix it with `update_datastage_flow` on that same `flow_id`. Never create a new flow and never delete the broken one; the id is what you edit against.

## Where to look

- **SDK conventions** (method signatures, stage config, link schemas, column types, connection binding, key rules, full example) → [references/sdk-conventions.md](references/sdk-conventions.md)
- **Stage selection** → `recommend_datastage_stages(subutterances=[...])`
- **Stage property names and accepted values** → `datastage_property_lookup(requests=[{"stage": "..."}])`
- **Per-stage deep-dive** → `di-agent-knowledge-engine-datastage` skill [stages/](../di-agent-knowledge-engine-datastage/stages/)
- **Flow optimization** → `di-agent-knowledge-engine-datastage` skill [optimization/overview.md](../di-agent-knowledge-engine-datastage/optimization/overview.md)
- **Custom stages (C/C++, Java)** → [BuildopStage.md](../di-agent-knowledge-engine-datastage/stages/BuildopStage.md), [JavaIntegrationStage.md](../di-agent-knowledge-engine-datastage/stages/JavaIntegrationStage.md)
- **Transformer stage expressions** → `di-agent-knowledge-engine-datastage` skill resource `stages/TransformerStageFunctions/TransformerStageFunctionsOverview.md`

## Editing

**Editing an existing flow:** In-place SDK edit is the right tool when the change is confined to expressions or stage properties on structure that already exists — retrieve the flow with `retrieve_datastage_flow_code`, change that SDK, and resubmit via `update_datastage_flow`. You are perturbing validated, already-wired code, so this is reliable, lossless, and cheap.

> **Edit the retrieved code — never hand-author a fragment.** Your `update_datastage_flow` submission must be the *complete* SDK returned by `retrieve_datastage_flow_code` with your additions spliced in, not a standalone snippet. Every stage, link, and schema you reference must be defined as a variable earlier in the same submission (the retrieved code already defines them — `derive_seg`, `veh_in`, `fp`, etc. — so reuse those variable names). The flattened SDK grammar has **no way to fetch existing elements**: `flow.links["x"]`, `flow.stages["y"]`, and `link.schema` are all rejected as "Unsupported statement type" / "variable does not exist". To add a column to an existing link, edit that link's existing `create_schema()`/`add_field(...)` lines in the retrieved code; to add structure, append new `flow.add_stage(...)` / `stage.connect_output_to(...)` / `link.create_schema()` statements that reference the already-defined variables. If a submission fails validation, fix the *whole* resubmitted code; do not re-fetch elements or re-author from scratch.

If the change instead adds or alters structure — a new source, a join, a different shape — do NOT hand-author it here from scratch; that is the SDK's least reliable path. Bootstrap the new structure in pyflow (`di-agent-flow-pyflow`), then precision-edit the generated SDK here to add anything pyflow can't express. If the core shape has no faithful pyflow form, bootstrap the closest shape pyflow can produce and reshape it here via `update_datastage_flow`.

**Versioning and backups** are owned by the lifecycle router's RECOVER state (`di-agent-flow-lifecycle/references/recover.md`). The short version: `update_datastage_flow` snapshots the flow automatically before it overwrites — you do **not** call `duplicate_asset` first, and doing so just leaves a stray copy. Up to 5 snapshots are kept per flow (the oldest is never discarded), they are hidden from `list_datastage_flows` by default, and they are deleted along with the flow.


## Guardrails

- **Fetch flows by `flow_id`** — `retrieve_datastage_flow_code` also accepts `flow_name`, but that path takes the first name-search match without checking it is unique, so an ambiguous name silently returns another flow's code
- **Never guess stage types, property names, or enum values** — use `recommend_datastage_stages` / `datastage_property_lookup`
- **Bundle all changes into a single submission** — successive submissions overwrite each other
- **`update_datastage_flow` never creates** — it errors if the named flow doesn't exist; verify the name via `list_datastage_flows`. To create, use `create_datastage_flow` (or pyflow) — see the lifecycle router for which
- **After a successful update**, surface the returned `flow_link` from the tool result as a clickable link so the user can open the flow in the UI
- **Stage property names in prose** — use the `User friendly name` from `datastage_property_lookup` (e.g. "Number of rows (per partition)"), not the internal identifier (`nrecs`); show the internal name only in code blocks or when the user asks for the SDK property
- **Parameterized flows:** `update_datastage_flow` loads the existing flow before rebuilding it, so parameter-set registrations and local parameters are preserved across SDK edits. If a job unexpectedly loses parameter bindings after an edit, call `get_flow_parameter_references` to audit what is registered and use `attach_parameter_set_to_flow` / `add_local_parameter` to restore any missing entries.
