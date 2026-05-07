# DataStage Generic Stage

## Purpose
Provide a flexible, customizable stage for executing user-defined operations and custom processing logic.

## When to Use
- Implementing custom processing logic not available in standard stages

## When NOT to Use
- When a standard stage can accomplish the task
- For simple transformations (use Transformer stage)

## Requirements
- **Link Cardinality**: any number of primary inputs

## Best Practices


## Property Configuration

### operator

Name of an Orchestrate operator to call

### inputlink_ordering_list

List of input links in the intended order. If there is one primary link and multiple reference links, re-ordering can occur only on reference links

```python
generic.configuration.inputlink_ordering_list = [{"link_label": "0", "link_name": "Link_1"}]
```