---
name: watsonx-data-integration-sdk
description: Use for editing existing flows, optimizing partitioning/sorting/memory on a specific flow, writing direct Python SDK scripts. Covers both DataStage batch and StreamSets streaming. For creating a NEW flow, prefer the `pyflow` skill.
---

# wx.di SDK

Python SDK for IBM watsonx Data Integration. Batch flows run on DataStage; streaming flows run on StreamSets — both through the same SDK.

## Invariants (apply to every path)

1. **Call `project.update_flow(flow)` after every change.** Changes are in-memory until persisted.
2. **Fetch batch flows by `flow_id`, never by name** — fetching by name returns incomplete stage data.
3. **For batch flows, call the `get_datastage_sdk_spec()` tool as the very first step.**
4. **Never guess stage types or property values.** Look them up:
   - Batch: `datastage_property_lookup(requests=[{"stage": "..."}])` or the `batch-datastage-engine` skill's [stages/](../batch-datastage-engine/stages/)
   - Streaming: `list_available_streaming_stages` + `list_all_available_stage_configurations_streaming`
5. **Validate before running.** `flow.compile()` for batch; `flow.validate()` for streaming.
6. **`execute_script` blocks `_` prefixed access.** No private attributes in sandboxed code.

---

## Pick a path

| Task | Start at |
|---|---|
| Edit an existing flow via MCP | [editing-flows.md](references/editing-flows.md) |
| Write and run a Python script against the SDK locally | [scripting-flows.md](references/scripting-flows.md) |
| Optimize an existing flow | `batch-datastage-engine` skill → [optimization/overview.md](../batch-datastage-engine/optimization/overview.md) |

Flow-type specifics (read alongside whichever path above):
- Batch (DataStage): [batch-datastage.md](references/batch-datastage.md) and always call the `get_datastage_sdk_spec()` tool before writing SDK code and read the relevant files in [stages/](../batch-datastage-engine/stages/)
- Streaming (StreamSets): [streaming-streamsets.md](references/streaming-streamsets.md)

Shared references (load on demand):
- Auth, collections, asset discovery, job lifecycle, column types, error stage → [sdk-conventions.md](references/sdk-conventions.md)
- Per-stage property/usage details (batch) → `batch-datastage-engine` skill [stages/](../batch-datastage-engine/stages/)
- Custom stages → [BuildopStage.md](../batch-datastage-engine/stages/BuildopStage.md) (C/C++), [JavaIntegrationStage.md](../batch-datastage-engine/stages/JavaIntegrationStage.md) (Java)

Working datastage examples: [examples/batch-datastage/](examples/batch-datastage/)
