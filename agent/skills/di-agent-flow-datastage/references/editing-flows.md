# Editing flows via MCP

DataStage batch flows are edited by retrieving their SDK code, modifying it, and resubmitting with overwrite enabled. The same submission tool creates flows from scratch when pyflow can't express them.

Read MCP tool descriptions at invocation time for exact names and parameters. This file covers workflow shape, not tool signatures.

---

## Workflows

**Edit an existing flow:**
1. Retrieve the flow's SDK code
2. Modify it
3. Submit with overwrite enabled
4. (optional) Run and poll

**Create a new flow (when pyflow can't express it):**
1. Read the SDK spec
2. Look up stage properties as needed (batch multiple stages per call)
3. Submit without overwrite
4. (optional) Run and poll

For new flows in general, prefer the `pyflow` skill.

---

## Rules

- Read the SDK spec before writing any SDK code.
- Look up every property before setting it — don't guess. Batch lookups across stages.
- Bundle multiple changes into one submission, not successive ones.
- Name collisions on submit-without-overwrite error out. Ask the user to overwrite or rename — **do NOT retry automatically**.
- Poll tools finish on their own; call once, not in a loop.

---

## Common edit patterns

**Change a stage property:** look up accepted values → edit `stage.configuration.<prop>` → resubmit.

**Insert a stage into a chain:** identify the linked pair → remove their connection → add and configure the new stage → reconnect `old_source → new_stage → old_target` → add schemas on the new links.

**Optimize an existing flow:** mechanics are identical; see the `di-common-engine-datastage` skill's [optimization/overview.md](../../di-common-engine-datastage/optimization/overview.md) for what to change.
