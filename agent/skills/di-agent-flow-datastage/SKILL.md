---
name: di-agent-flow-datastage
description: "Reference for creating DataStage (batch) flows with the watsonx.data integration SDK. The SDK is verbose and permits exhaustive stage and property access: use it to author flows pyflow's compact DSL can't express, and to edit or optimize existing DataStage flows, including ones bootstrapped with pyflow."
---

# Create / Edit DataStage Flows

DataStage batch flows are authored by writing SDK-style Python code and submitting
via `create_or_update_datastage_flow`. Auth, project context, persistence, and
compilation are handled automatically.

## Where to look

- **SDK conventions** (method signatures, stage config, link schemas, column types, connection binding, key rules, full example) → [references/sdk-conventions.md](references/sdk-conventions.md)
- **Stage selection** → `recommend_datastage_stages(subutterances=[...])`
- **Stage property names and accepted values** → `datastage_property_lookup(requests=[{"stage": "..."}])`
- **Per-stage deep-dive** → `di-agent-knowledge-engine-datastage` skill [stages/](../di-agent-knowledge-engine-datastage/stages/)
- **Flow optimization** → `di-agent-knowledge-engine-datastage` skill [optimization/overview.md](../di-agent-knowledge-engine-datastage/optimization/overview.md)
- **Custom stages (C/C++, Java)** → [BuildopStage.md](../di-agent-knowledge-engine-datastage/stages/BuildopStage.md), [JavaIntegrationStage.md](../di-agent-knowledge-engine-datastage/stages/JavaIntegrationStage.md)

## Versioning

Use `duplicate_asset(asset_id=..., asset_type="datastage_flow", project_id=...)` as a safety net before making changes that could break a flow.

**Editing an existing flow:** Before modifying, duplicate the flow as a backup with a timestamped name (`"{name} [backup YYYY-MM-DD]"`). Work on the original — the backup is your rollback point. Keep at most one backup per flow to avoid clutter (delete old ones via `delete_asset`).

**Iterating on a new flow:** After a successful `create_or_update_datastage_flow`, if the user requests further edits, snapshot the working state first via `duplicate_asset`. This way you can restore if subsequent changes break it.

**Restoration:** Not a single tool call. Delete the broken flow, then duplicate the backup back to the original name — or simply point the user to the backup.

**Caveats:** Duplicating a flow does NOT duplicate any jobs or schedules attached to it. Be cautious when editing flows with active job runs. Cross-flow references (e.g. sub-flows) are not preserved in the backup.

## Guardrails

- **Fetch flows by `flow_id`**, never by name — name returns incomplete stage data
- **Never guess stage types, property names, or enum values** — use `recommend_datastage_stages` / `datastage_property_lookup`
- **Bundle all changes into a single submission** — successive submissions overwrite each other
- **Name collisions on create** — ask user to confirm overwrite or rename, never retry automatically
- **After a successful create/update**, surface the returned `flow_link` from the tool result as a clickable link so the user can open the flow in the UI
- **Stage property names in prose** — use the `User friendly name` from `datastage_property_lookup` (e.g. "Number of rows (per partition)"), not the internal identifier (`nrecs`); show the internal name only in code blocks or when the user asks for the SDK property
