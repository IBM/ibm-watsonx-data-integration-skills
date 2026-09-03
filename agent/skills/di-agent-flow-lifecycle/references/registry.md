# Authoring backends

Read by the AUTHOR state (`author.md`). AUTHOR does not run an if/else over backends: it defaults to **pyflow** and leaves it only when a fallback backend's selection trigger fires.

There is deliberately no list of supported stages. pyflow is declarative and the compiler picks the stages, so the routing question is "can this backend express the request?", not "is this stage on a list". The only lists below are the known **gaps**.

## pyflow — the default, try this first

| | |
|---|---|
| Load | `di-agent-flow-pyflow` |
| Engines | DataStage, StreamSets |
| Operations | create; edit via `create_pyflow(replace_flow_id=<id>)`, which overwrites in place |
| Works from | the user's goal, stated declaratively — the compiler picks the stages |
| Needs | the user's intent, **not** stage expertise; this is why it is the default |
| Coverage | broad and declarative — escalate only when a request is not expressible |
| Validation | **pre-publish** — the DSL is compiled and IR-validated before any asset exists, then the published flow is compiled on the engine |
| Escalates to | `datastage-sdk`, on DataStage only |
| Cost | low |

### Known gaps — DataStage

The gaps are split by what each one does to **routing**, not by what kind of stage it is. That split is the point: a gap is not a reason to abandon pyflow unless it stops pyflow producing a backbone worth keeping.

**Blocking — pyflow cannot lay a useful backbone at all.** The gap sits at the source position, or it defines the flow's whole shape, so a pyflow attempt would produce a scaffold you would have to *rewire* rather than add to. Go straight to `datastage-sdk` for the create; do not attempt pyflow first.

At the source position — there is no upstream for pyflow to build from:

- **Row Generator stage** — mock or generated rows; pyflow needs real data first
- **REST stage as the flow's source** — data from a REST API call feeding the flow

Structural — these decide how the flow is shaped or wired:

- **Lookup** — combines two inputs; pyflow rejects `.lookup()` on DataStage
- **Subflows** — a nested flow *is* the structure
- **DataStage components** — shared reusable components: referenced, not authored
- **Flow-level connections** — pyflow binds per source; it has no flow-scoped connection model

**Spliceable — pyflow builds the backbone fine and the gap is local.** One stage hung off the flow, or a property or expression on a stage that already exists. This is the common case and it is **not** an escalation: author in pyflow, then splice via `retrieve_datastage_flow_code` → `update_datastage_flow`. See `author.md` Step 2, outcome (b).

Processing stages, which hang off a backbone pyflow builds:

- Bloom Filter
- Change Apply — the backbone must carry both inputs
- Change Capture — the backbone must carry both inputs
- Checksum
- Compress
- Difference — the backbone must carry both inputs
- Expand
- Generic
- Java Integration
- Peek
- Pivot Enterprise
- REST mid-flow, where it is not the source
- Slowly Changing Dimension
- Stored Procedure
- Surrogate Key Generator
- Wave Generator
- Web Service
- Buildop — a custom C/C++ stage

Restructuring stages:

- Column Export
- Column Import
- Combine Records
- Make Subrecord
- Make Vector
- Promote Subrecord
- Split Vector

Data quality stages:

- Data Rules
- Investigate
- Match Frequency
- One Source Match
- Standardize
- Two Source Match

**Spliceable stage features** are not stages at all — they are properties and expressions *on* a stage pyflow already emits. These are the weakest possible reason to leave pyflow: the structure is already right and one measure or derivation needs the SDK.
- **Aggregator measures with no pyflow form** — Corrected Sum of Squares, Missing Values, Missing Values Count, Non-Missing Values Count, Percent Coefficient of Variation, Preserve Type, Range, Standard Deviation, Standard Error, Sum of Weights, Summary, Uncorrected Sum of Squares, Variance, Weighting.
- **Transformer functions** — any transformer function with no pyflow equivalent. Complex derivation expressions are spliced into the generated SDK once the structure exists.
- **Connectors** — connector coverage is not fully verified, especially for creating new tables. An unverified connector may need an SDK correction after the pyflow compile; that is a splice, not a reason to skip pyflow.

**Absence from these lists is not a promise of support.** Parameter sets and local parameters are deliberately absent, though: pyflow supports them, via `create_pyflow(parameters=…)` and `#token#` bindings.

### Known gaps — StreamSets

None are enumerated. That is not a promise that pyflow covers everything on StreamSets.

There is also nowhere to send a StreamSets gap. The only other backend is DataStage-only, so on StreamSets pyflow is the **only** option: a gap there is a limit to report to the user, not a routing decision. See `author.md` Step 1.

## datastage-sdk — the fallback and escape hatch, DataStage only

| | |
|---|---|
| Load | `di-agent-flow-datastage` |
| Engines | DataStage |
| Operations | create via `create_datastage_flow`; edit via `update_datastage_flow` |
| Works from | an existing flow — usually an edit or extension, often of a pyflow scaffold |
| Needs | exact stage types, property names, and enum values |
| Coverage | the full engine stage catalog, via `di-agent-knowledge-engine-datastage` |
| Validation | **on save** — create and update compile the flow as part of the call |
| Cost | high |

### Select this backend when

Any one of these is enough on its own. A **spliceable** gap is deliberately not on the list: splicing keeps the pyflow backbone and is the default for local gaps, per `author.md` Step 2.

- The user explicitly asks for the SDK, or names a stage that decides the flow's shape. Naming a *property* never leaves pyflow.
- The request is not expressible in pyflow at all, including anything on the blocking list above.
- Several structural stages are named at once.
- There are no data sources upfront — a mock-data flow, which pyflow has nothing to build from.
- One flow has to produce several file assets.
- Pyflow has already failed five or more times on this same request.

## Nothing else is selectable

These two backends are the whole registry, and both are stable. Nothing experimental is registered, so there is no "ask the user first" tier to fall back on: a backend not described above is not selectable, and a request for one is a capability limit to report rather than a backend to reach for.
