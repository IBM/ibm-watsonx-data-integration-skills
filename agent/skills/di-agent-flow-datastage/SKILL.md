---
name: di-agent-flow-datastage
description: "Reference for the verbose watsonx.data integration SDK for DataStage (batch) flows, with exhaustive stage and property access. New flows can only be created with pyflow's compact DSL (`di-agent-flow-pyflow`); use this SDK to edit existing flows in place — for what pyflow can't express."
---

# Edit DataStage Flows

Existing DataStage batch flows are edited by writing SDK-style Python code and
submitting via `update_datastage_flow`. Auth, project context, persistence, and
compilation are handled automatically.

New flows cannot be created through the SDK surface: create them with pyflow
(`di-agent-flow-pyflow` / `create_pyflow`), then edit in place here when a change
needs something pyflow can't express.

## Where to look

- **SDK conventions** (method signatures, stage config, link schemas, column types, connection binding, key rules, full example) → [references/sdk-conventions.md](references/sdk-conventions.md)
- **Stage selection** → `recommend_datastage_stages(subutterances=[...])`
- **Stage property names and accepted values** → `datastage_property_lookup(requests=[{"stage": "..."}])`
- **Per-stage deep-dive** → `di-agent-knowledge-engine-datastage` skill [stages/](../di-agent-knowledge-engine-datastage/stages/)
- **Flow optimization** → `di-agent-knowledge-engine-datastage` skill [optimization/overview.md](../di-agent-knowledge-engine-datastage/optimization/overview.md)
- **Custom stages (C/C++, Java)** → [BuildopStage.md](../di-agent-knowledge-engine-datastage/stages/BuildopStage.md), [JavaIntegrationStage.md](../di-agent-knowledge-engine-datastage/stages/JavaIntegrationStage.md)
- **Transformer stage expressions** → `di-agent-knowledge-engine-datastage` skill resource `stages/TransformerStageFunctions/TransformerStageFunctionsOverview.md`

## Versioning

Use `duplicate_asset(asset_id=..., asset_type="datastage_flow", project_id=...)` as a safety net before making changes that could break a flow.

**Editing an existing flow:** In-place SDK edit is the right tool when the change is confined to expressions or stage properties on structure that already exists — retrieve the flow with `retrieve_datastage_flow_code`, change that SDK, and resubmit via `update_datastage_flow`. You are perturbing validated, already-wired code, so this is reliable, lossless, and cheap.

> **Edit the retrieved code — never hand-author a fragment.** Your `update_datastage_flow` submission must be the *complete* SDK returned by `retrieve_datastage_flow_code` with your additions spliced in, not a standalone snippet. Every stage, link, and schema you reference must be defined as a variable earlier in the same submission (the retrieved code already defines them — `derive_seg`, `veh_in`, `fp`, etc. — so reuse those variable names). The flattened SDK grammar has **no way to fetch existing elements**: `project.flows.get(...)`, `flow.links["x"]`, `flow.stages["y"]`, and `link.schema` are all rejected as "Unsupported statement type" / "variable does not exist". To add a column to an existing link, edit that link's existing `create_schema()`/`add_field(...)` lines in the retrieved code; to add structure, append new `flow.add_stage(...)` / `stage.connect_output_to(...)` / `link.create_schema()` statements that reference the already-defined variables. If a submission fails validation, fix the *whole* resubmitted code; do not re-fetch elements or re-author from scratch.

If the change instead adds or alters structure — a new source, a join, a different shape — do NOT hand-author it here from scratch; that is the SDK's least reliable path. Bootstrap the new structure in pyflow (`di-agent-flow-pyflow`), then precision-edit the generated SDK to add anything pyflow can't express — an unsupported function, or an extra stage spliced in. If the core shape has no faithful pyflow form, bootstrap the closest shape pyflow can produce, then reshape it here via `update_datastage_flow`.

Backups are optional and cost tool calls — only duplicate as a rollback point when the user values the existing flow as something to protect (an established production flow they asked you to change carefully). Skip the backup for a one-shot "finish it / fix it and run it" request on a partial or scratch flow: just retrieve, edit, resubmit, and run. When you do back up, use a timestamped name (`"{name} [backup YYYY-MM-DD]"`), work on the original, and keep at most one backup per flow (delete old ones via `delete_asset`). Do not spend calls duplicating, deleting, or re-duplicating while you are still trying to get a single edit to validate.

**Iterating on a new flow:** Once a freshly bootstrapped flow reaches a working state, if the user requests further edits, snapshot the working state first via `duplicate_asset`. This way you can restore if subsequent changes break it.

**Restoration:** Not a single tool call. Delete the broken flow, then duplicate the backup back to the original name — or simply point the user to the backup.

**Caveats:** Duplicating a flow does NOT duplicate any jobs or schedules attached to it. Be cautious when editing flows with active job runs. Cross-flow references (e.g. sub-flows) are not preserved in the backup.

## Guardrails

- **Fetch flows by `flow_id`**, never by name — name returns incomplete stage data
- **Never guess stage types, property names, or enum values** — use `recommend_datastage_stages` / `datastage_property_lookup`
- **Bundle all changes into a single submission** — successive submissions overwrite each other
- **`update_datastage_flow` never creates** — it errors if the named flow doesn't exist; verify the name via `list_datastage_flows`, and create new flows with pyflow
- **After a successful update**, surface the returned `flow_link` from the tool result as a clickable link so the user can open the flow in the UI
- **Stage property names in prose** — use the `User friendly name` from `datastage_property_lookup` (e.g. "Number of rows (per partition)"), not the internal identifier (`nrecs`); show the internal name only in code blocks or when the user asks for the SDK property
