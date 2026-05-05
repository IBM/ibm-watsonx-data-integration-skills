# Streaming flows (StreamSets)

Streaming-specific nuances. Read alongside [scripting-flows.md](scripting-flows.md).

Streaming flows are edited via the direct SDK — there is no MCP-submission path equivalent to `create_or_update_datastage_flow`.

## Engine pre-flight

Before creating a streaming flow:

1. If the user passed an engine ID or engine → verify `health.status == 'online'`; if not, report it
2. If the user passed an environment or environment_id → check for an online engine in that environment; use if available
3. If no engine/environment passed, OR no online engines → proceed in **engineless mode** (pass `environment=None`). The platform backend uses an engineless designer and provides all stages/configs.

```python
engines = project.engines.get_all()
for e in engines:
    print(e.engine_id, e.health.status)   # 'online' or 'lost'
```

Then always discover available stages via MCP before authoring — never guess stages.

## Creating a streaming flow

```python
# With environment
env = project.environments.get_all()[0]
flow = project.create_flow(name='My Flow', environment=env)

# Engineless mode
flow = project.create_flow(name='My Flow', environment=None)

# flow_type defaults to 'streaming' — do not specify
```

## Stage discovery — runtime via MCP

Streaming stages are discovered dynamically. The `execute_script` sandbox blocks `_` prefixed access, so private SDK attributes are not an option — use MCP tools.

```
# Step 1: discover available stage labels
list_available_streaming_stages(flow_id=..., project_id=...)

# Step 2: get configs for specific stages (batch 5–8 at a time — never all at once)
list_all_available_stage_configurations_streaming(
    flow_id=..., project_id=...,
    stage_labels=['Stage A', 'Stage B', ...],
)
```

Fetching configs for every stage at once will exceed the context window and be written to disk. Parse disk results with:

```python
import json
with open('/path/to/result.json') as f:
    data = json.load(f)
configs = json.loads(data[0]['text'])   # content is nested inside data[0]['text']
```

## Validation

```python
project.update_flow(flow)        # persist changes first
result = flow.validate()         # NOT project.validate_flow(flow) — that doesn't exist

if result.issues:
    for issue in result.issues:
        print(issue.instance_name, issue.human_readable_message)
else:
    print("Validation passed")
```

`project.validate_flow(flow)` does not exist. The correct method is `flow.validate()`.

## Stream Selector pattern

Multiple-predicate routing, streaming-only:

```python
selector = flow.add_stage('Stream Selector')
selector.add_predicates([
    '${record:value("/type") == "A"}',
    '${record:value("/type") == "B"}',
])
selector.connect_output_to(handler_a, predicate=selector.predicates[0])
selector.connect_output_to(handler_b, predicate=selector.predicates[1])
```

## Offset management

Streaming-only:

```python
job.reset_offset()
```
