---
name: di-agent-flow-datastage
description: Create or edit DataStage batch flows via platform MCP tools. Use when the user wants to create a new flow that di-agent-flow-pyflow can't express, edit or extend an existing flow, or optimize a specific flow's configuration. DataStage only — for StreamSets flows use the di-agent-flow-pyflow skill.
---

# Create / Edit DataStage Flows

DataStage batch flows are authored by writing SDK-style flow code and submitting it via the platform MCP tool. The tool handles project context, auth, and persistence — no boilerplate required.

For new flows expressible as simple source → transform → sink pipelines, prefer the `di-agent-flow-pyflow` skill. Use this skill when pyflow can't express the flow (complex stage graphs, native stage properties, editing existing flows).

## Invariants

1. **Read the SDK spec first.** Call `get_datastage_sdk_spec()` before writing any flow code.
2. **Fetch existing flows by `flow_id`, never by name** — fetching by name returns incomplete stage data.
3. **Never guess stage types or property values.** Look them up: `datastage_property_lookup(requests=[{"stage": "..."}])` or the `di-common-engine-datastage` skill's [stages/](../di-common-engine-datastage/stages/).
4. **Validate before running.** `flow.compile()`.
5. **Bundle all changes into one submission** — not successive ones.

## Workflows

**Edit an existing flow:**
1. Retrieve the flow's SDK code
2. Modify it
3. Submit with overwrite enabled
4. (optional) Run and poll

**Create a new flow:**
1. Read the SDK spec
2. Look up stage properties as needed (batch multiple stages per call)
3. Submit without overwrite
4. (optional) Run and poll

Name collisions on submit-without-overwrite error out. Ask the user to overwrite or rename — **do not retry automatically**.

Poll tools finish on their own — call once, not in a loop.

## References

- Workflow detail, edit patterns → [references/editing-flows.md](references/editing-flows.md)
- Stage configuration, link schemas, column types, job lifecycle → [references/batch-datastage.md](references/batch-datastage.md) and [references/sdk-conventions.md](references/sdk-conventions.md)
- Per-stage property details → `di-common-engine-datastage` skill [stages/](../di-common-engine-datastage/stages/)
- Custom stages → [BuildopStage.md](../di-common-engine-datastage/stages/BuildopStage.md) (C/C++), [JavaIntegrationStage.md](../di-common-engine-datastage/stages/JavaIntegrationStage.md) (Java)
- Flow optimization → `di-common-engine-datastage` skill [optimization/overview.md](../di-common-engine-datastage/optimization/overview.md)
