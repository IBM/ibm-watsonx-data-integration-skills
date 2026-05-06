---
name: di-sdk-streaming-flows
description: Build and run StreamSets streaming flows via the Python SDK — engine pre-flight, stage discovery, configuration rules, connecting stages, and flow validation.
---

# Streaming flows

---

## Engine pre-flight check

Your first action item should be to see if the user provided an engine ID or an environment. Follow this framework:
1. If the user passed an engine or engine_id, verify that the engine is online, if it is not online let the user know
2. If the user has passed an environment or environment_id, check if there are available online engines within the environment and use that
3. If no engine or environment has been passed OR if there are no available online engines, you can proceed in engineless mode. This means that you can create a streaming flow within a project without an engine (the platform backend will proceed in an engineless designer mode and provide you with all stages and configs needed)

Once done, always check what available stages are there before proceeding with flow creation. DO NOT GUESS STAGES — use `list_available_streaming_stages` and `list_all_available_stage_configurations_streaming`.

```python
engines = project.engines.get_all()
for e in engines:
    print(e.engine_id, e.health.status)  # 'online' or 'lost'
```

---

## Complete workflow

Follow this order exactly:

```
1.  authenticate         → Detect auth type (IAMAuthenticator, ICP4DAuthenticator, or ZenApiKeyAuthenticator) + Platform
2.  get project          → platform.projects.get(project_id=...)
3A. engine check         → project.engines.get_all() — verify health.status == 'online'
3B. get environment      → project.environments.get_all() — needed to create a flow
4.  get or create flow   → project.flows.get(name=...) or project.create_flow(name=..., environment=env)
6.  discover stages      → list_available_streaming_stages (MCP tool)
7.  get configs for necessary stages          → list_all_available_stage_configurations_streaming (MCP tool, in small batches)
8.  add stages           → flow.add_stage(label=..., type=...)
9.  configure stages     → print(stage.configuration), then set fields using accepted_values
10. connect stages       → origin.connect_output_to(destination)
11. update flow          → project.update_flow(flow)
12. validate flow        → flow.validate() — check ValidationResult.issues before proceeding
13. create job           → project.create_job(name=..., flow=flow)
14. start job            → job_run = job.start()
```

---

## Creating a streaming flow (requires environment)

```python
# Environment is not REQUIRED to create a streaming flow / you can just pass None into environment parameter to enter engineless mode
env = project.environments.get_all()[0]
flow = project.create_flow(name='My Flow', environment=env)

# Streaming flows do NOT need flow_type= specified (it defaults to 'streaming')
```

---

## Stage discovery

Use MCP tools — do not call private SDK attributes in `execute_script` (the sandbox blocks `_` prefixed access):

```python
# Step 1: Discover available stage labels
# → Call MCP tool: list_available_streaming_stages(flow_id=..., project_id=...)

# Step 2: Get configs for specific stages (do in batches of 5-8, NOT all at once)
# → Call MCP tool: list_all_available_stage_configurations_streaming(
#       flow_id=..., project_id=..., stage_labels=['Stage A', 'Stage B', ...]
#   )
```

> ⚠️ Fetching configs for all stages at once will exceed the context window and be written to disk. Batch your requests to 5–8 stages at a time.

When the result is stored to a file path, parse it with:
```python
import json
with open('/path/to/result.json') as f:
    data = json.load(f)
configs = json.loads(data[0]['text'])  # the actual content is nested inside data[0]['text']
```

---

## Stage configuration rules

```python
stage = flow.add_stage(label='Kafka Multitopic Consumer', type='origin')
print(stage.configuration)   # always inspect before setting anything

# Set by key (camelCase or snake_case both work)
stage.configuration['key_capture_mode'] = 'RECORD_HEADER'  # dict-style
stage.configuration.key_capture_mode = 'RECORD_HEADER'     # dot-style

# If accepted_values is non-empty, you MUST use one of those values exactly
# Never invent or guess enum values
```

**Write to File error stage**: has `directory`, `max_file_size_in_mb`, `file_wait_time_in_secs`, and `files_prefix`. The error stage shortcut is `flow.set_error_stage('Write to File')`.

---

## Connecting stages

```python
# Basic connection
origin.connect_output_to(destination)
destination.connect_input_to(origin)    # equivalent

# Chaining
origin.connect_output_to(processor).connect_output_to(destination)

# Fan-out (one stage to many)
origin.connect_output_to(proc1, proc2, proc3)

# Stream Selector (multiple predicates)
selector = flow.add_stage('Stream Selector')
selector.add_predicates(['${record:value("/type") == "A"}', '${record:value("/type") == "B"}'])
selector.connect_output_to(handler_a, predicate=selector.predicates[0])
selector.connect_output_to(handler_b, predicate=selector.predicates[1])

# Event output
origin.connect_event_to(pipeline_finisher)
```

---

## Validating a flow

```python
project.update_flow(flow)        # persist changes first
result = flow.validate()         # NOT project.validate_flow(flow) — that doesn't exist

if result.issues:
    for issue in result.issues:
        print(issue.instance_name, issue.human_readable_message)
else:
    print("Validation passed")
```

> `project.validate_flow(flow)` does **not** exist — the correct method is `flow.validate()`.
