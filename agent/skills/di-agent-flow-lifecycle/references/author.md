# AUTHOR state

## Entry

The intent is to create or change a flow's structure or content. A target flow may or may not already exist.

**Author the flow; do not interview the user about it.** Requests arrive underspecified — "some sample customer records", "flag districts below the state mean" — and the missing pieces (which columns the generated rows have, which numeric column the mean is over, whether the mean is computed in-flow or supplied) are yours to choose. Choose them, build the flow, and name your choices when you report it: a wrong guess costs the user one sentence to correct, while a question costs a whole turn and often ends the task with nothing built. Handing back a description of the flow you *would* build is the most expensive failure in this state — it burns the budget and leaves no asset behind. Ask only when the **target** is ambiguous (two existing flows or assets match and editing the wrong one destroys work); never ask for a schema, a column, a name, or a value you can invent.

## Step 0 — Verify every source column against the asset, before writing anything

**Do not write a column name you have not read from the asset.** For each source the flow reads, call `inspect_project_asset(asset_type="data_asset", …)` and take the authoritative column list — `{name, type, nullable}` — from it. Only those names may appear in the flow you author: in `q.source()` and `q.col()` on the pyflow path, in the schema and derivation code on the SDK path.

This applies to **both backends**. It is the cheapest step in this state and it prevents the most common authored-flow defect: a column name that was guessed, carried over from a similar flow, or inferred from the user's phrasing.

- The names in a user's request are a description, not a schema. "Customer name" may be `CUST_NM`.
- A column can exist and still be unusable if its **type** is wrong for what you are doing with it — read the type, do not assume it from the name.
- Output/derived column names you invent are fine. This rule is about **input** columns.
- `list_data_assets` finds an asset; it does not give you its schema. Its `columns` list is names only, from a search index that may be stale. Finding the asset is not verifying its columns.

A guessed column does not fail at author time on the SDK path — it compiles, runs, and produces a run failure or silently wrong output that DIAGNOSE then has to chase back here. Verifying up front costs one call per source.

## Step 1 — CREATE or EDIT? (precedence rule 3)

- **No target flow** → CREATE path.
- **Target flow exists** → EDIT path. Never fall through to a new create to "redo" a flow.

The mechanics on the EDIT path turn on one question: **do you have this flow's real definition, or only a description of it?**

| Situation | What to call |
|---|---|
| Editing a flow you authored **in pyflow this session** (you still have the DSL) | `create_pyflow(..., replace_flow_id=<the id>)` — re-emit the full DSL with the change, overwrite in place, keeping id and name |
| Editing a flow you did **not** author in pyflow — anything already in the project, or one you built via the SDK | `retrieve_datastage_flow_code` → splice the change into that code → `update_datastage_flow` (Step 4). This holds whether the change is an expression tweak or a new source/join. |
| The user explicitly asks to rebuild the flow from scratch | Author fresh from the goal, then land it with `create_pyflow(replace_flow_id=<the id>)`. A rebuild is still an in-place overwrite — the flow exists, so it keeps its id |

**Editing an existing flow means editing the definition it already has — not replacing it with your best reconstruction.** `create_pyflow(replace_flow_id=…)` overwrites the flow with *whatever DSL you submit*, so pointing it at a flow you did not author in pyflow means rebuilding from your reading of its SDK code, and every stage or property you don't perfectly reproduce is silently dropped. Splicing into the real code (Step 4) preserves everything you didn't touch, which is why it is the default for existing flows. Reach for `replace_flow_id` only when the DSL you'd submit *is* the flow's true source, or when the user wants a rebuild.

`create_pyflow` **without** `replace_flow_id` always mints a new asset. Deleting the old flow and recreating it is not an edit — it churns assets and loses the id, taking every job pointing at that flow with it.

**On StreamSets the splice path does not apply.** `retrieve_datastage_flow_code` and `update_datastage_flow` are DataStage-only, and no SDK backend is registered for StreamSets — so `create_pyflow(replace_flow_id=…)` is the only edit path there. If you hold the DSL from this session, re-emit it with the change. If you do not, say so and ask the user what the flow should do, rather than reconstructing a definition you cannot read: on this engine there is nothing to splice into and no way to check what you dropped.

> **Why pyflow has one tool and the SDK has two.** pyflow targets a flow by **id**, so `replace_flow_id` present/absent is unambiguous. The SDK targets by **name**, which you can be wrong about, so intent is carried by *which tool you call* and each one checks it: `create_datastage_flow` refuses a name that is taken, `update_datastage_flow` refuses one that is free. Either refusal means you had the state wrong — re-read it and call the other tool; do not work around it.

If a job is currently running against the target flow, say so and confirm with the user before overwriting.

## Step 1b — The rollback point is automatic

Overwrite-in-place is destructive and the platform keeps no version history — but **you do not need to snapshot manually.** Both in-place edit paths (`create_pyflow(replace_flow_id=…)` and `update_datastage_flow`) take the snapshot for you before they change anything:

- the flow is duplicated to `"{name}Backup{YYYYMMDDHHMMSS}"` (e.g. `ordersBackup20260723143025`);
- up to 5 snapshots are kept per flow and the **oldest is never discarded**, so the pre-edit original stays reachable however many times you edit;
- the result carries `backup_flow_id` / `backup_flow_name` for this snapshot, and `backups` — the full surviving history, oldest first;
- if the snapshot cannot be taken, the edit is **refused** and the flow is left unchanged. Retry the same call. Do **not** work around it by creating a new flow;
- retrying a rejected save does **not** stack up snapshots: one taken moments ago is reused (`backup_reused` instead of `backup_created`), and one taken for a save that then failed is removed again. So the rollback point you end a fix-and-resubmit loop with is the flow as it stood before the loop began — which is the one worth having.

**Do not tell the user a backup was created when the result says `backup_reused`.** It is still their rollback point and still worth mentioning, but "I created a backup" is a claim about something that did not happen this time.

So do not call `duplicate_asset` yourself before an edit — you would end up with two backups. Use it only for the deliberate cases in `recover.md` (keeping a named copy the user asked for).

## Step 2 — Select a backend (`registry.md`)

**Default to `pyflow` and try it first.** It is declarative — express *what the user wants* and let the compiler choose stages; you do not need stage-level DataStage knowledge to start. It also compiles and validates the DSL before any asset exists, so most failures are caught pre-publish.

**Decide the backend from the triggers below, not by probing.** They are answerable from the request itself — whether the user named a stage, whether sources exist, and which of pyflow's gap lists — **blocking** or **spliceable** — the named thing falls on. `datastage_property_lookup` and `recommend_datastage_stages` describe stages you have already chosen to use; reaching for them to work out *whether* pyflow can do something inverts the order and spends the task's budget before authoring starts. Look properties up when you write the stage, not when you pick the path.

### There are THREE outcomes here, not two

The common mistake is treating this as pyflow-or-SDK. Most capability gaps are **local** — one stage or one property on a flow that pyflow otherwise builds correctly — and the right answer for those is *both*: a pyflow backbone with an SDK splice on top. Pick one of:

| Outcome | When | What you do |
|---|---|---|
| **(a) pyflow** | nothing in the request is a known gap | author the whole flow in pyflow |
| **(b) pyflow → splice** | the gap is on pyflow's **spliceable** list — a stage hung off the flow, or a property/expression/aggregate on a stage that already exists | author the backbone in pyflow, then splice the rest onto the generated SDK (Step 4) |
| **(c) datastage-sdk** | a selection trigger fires — see below | author the whole flow with the SDK |

**(b) is a first-class outcome, not a recovery.** It is the default for every **spliceable** gap, and it is chosen *here*, before you author — not discovered in Step 4 after something fails. Hand-writing a source, join, or the wiring between them is the SDK's least reliable path; pyflow lays that backbone correctly every time and leaves you a small, local edit. Never take (c) for a flow that is mostly pyflow-shaped.

This fork is **DataStage-only**: on StreamSets, pyflow is the only registered backend, so there is no (b) or (c). A StreamSets request pyflow cannot express is a limit to report to the user, not a backend to switch to.

Escalate to **`datastage-sdk`** — outcome (c) — only when one of the triggers under its "Select this backend when" heading fires. **Read those triggers, and the blocking / spliceable lists they refer to, from `registry.md`** — they are not restated here. On a **blocking** gap, skip the pyflow attempt entirely and go straight to the SDK.

The rest of this step is what the registry cannot encode — how to read a request against those lists.

### Structural or local? — the question that decides (b) vs (c)

"The user named a stage" is too blunt on its own. What matters is **what the named thing does to the flow's shape** — which is exactly what the registry's two gap lists encode:

- **Structural** — it sits at the *source* position, or it decides how data is combined or routed. These are pyflow's **blocking** list. pyflow cannot lay a backbone you would keep → **(c)**.
- **Local** — it hangs off a shape pyflow can build, or it is a property, expression, aggregate measure, or transformer derivation on a stage that already exists. pyflow's **spliceable** list → **(b)**.

**Naming a property never leaves pyflow.** "A basic sort flow, but set this specific property on the target" is outcome (b): pyflow builds the sort flow, the SDK sets the property. Sending that to the SDK means hand-authoring an entire flow to change one field. A *single* missing function, property, or stage is never an escalation trigger by itself. When in doubt, pick (b): a wrong pyflow attempt costs one compile, an unnecessary full-SDK build costs the whole flow.

### Call out what you cannot do, then do your best on the rest

Requests arrive with parts that do not apply here — a build path or format not in the registry, an option carried over from another product, a feature this engine lacks. **Name those parts, then build the rest.** Both halves matter: reporting without building is the interview failure this state bans, and building without reporting leaves the user believing they got what they asked for.

Not recognising the name is the normal case, not a reason to hesitate — a name absent from the skills is a name that does not apply. Do not make it fit by mapping it onto the nearest thing you do recognise; that is how the user ends up never told.

Say which part you could not do, in their own word for it, **before** describing what you built — a reply that opens with the flow has already moved past the question. If the unsupported part *was* the request, so anything you built would not be what was asked for, say so and stop instead of substituting.

This overrides "outcome (a) needs no announcement" below, which assumes the user expressed no preference about how the flow gets built.

### Say why, when the backend is not the default

Outcome (a) is the default, so it needs no announcement. **Outcomes (b) and (c) each need one sentence naming the capability that forced them, in the user's terms.** Name the capability and what you did about it — and **do not name a builder**, not "pyflow", not "the SDK", and not a friendly stand-in for either. The user does not have two builders to choose between, so introducing one only raises a question you then have to answer.

> (c): "This flow needs a stage that generates rows from scratch, which I can't set up automatically — so I built it out stage by stage."
>
> (b): "The flow is built. That one setting on the target isn't covered automatically, so I set it on the stage directly."

**Put it in the message you send the user, and specifically in the last one** — that message is the only thing they read. Saying it in an earlier message and dropping it from the summary does not count. There is no slot for narration between tool calls: if it is not in the reply, you did not say it.

Say it **even when nothing went wrong**. This is the failure mode that actually happens: the router works, you go straight to the right path on the first try, and because the build was clean it never occurs to you that anything needs explaining. But a capability limit — not a preference — shaped the user's flow, and that sentence is their only signal. A flow that was built without incident on the non-default path still needs it.

When the *user* named the SDK, confirm it back the same way. When you escalate *after* a failed attempt, say what the flow needed that could not be built the default way; switching silently after an error is indistinguishable from flailing.

Say it in product terms — what the *flow* needed. Naming the machinery ("pyflow", "the SDK", "the backend") is the same fact leaked as jargon, and fails the rule just as silence does.

## Step 3 — Author with the selected backend

Load the skill named in the backend's **Load** row in `registry.md` — the one you **selected**, and only that one — the other is a large reference for a path already ruled out. Step 2 chose; this step executes.

- **pyflow — create:** write the DSL for the user's goal, then `create_pyflow`, then `rename_asset` — a create publishes with a random suffix (`orders_a4bc9z1q`), so it is not finished until the rename lands. Rename before any job or run, and even if the flow failed to compile: the suffixed flow is what stays behind either way. The backend skill has the call signature.
- **pyflow — edit:** write the DSL for the *whole intended flow* and call `create_pyflow(replace_flow_id=<id>)`. The id and name are preserved, so no rename is needed.
- **pyflow → splice (outcome b):** author the backbone as above, then continue straight into Step 4 — the flow is not finished until the splice lands. This is **one** AUTHOR pass with a two-phase authoring step, not a second lap through the router: re-entering the router would classify the now-existing flow as a fresh EDIT and put you back in duplicate territory.
- **datastage-sdk — create:** `create_datastage_flow` with the complete SDK body.
- **datastage-sdk — edit:** see Step 4.

## Step 4 — The splice path (SDK edit, and pyflow-scaffold → SDK)

Use this when Step 2 picked outcome (b) and pyflow has laid the backbone, or when you are making a property/expression-level edit to an existing flow.

1. `retrieve_datastage_flow_code` for the whole flow — pass `flow_id`, not `flow_name`. The name path resolves through a name search and takes the first match without checking it is unique, so an ambiguous name silently returns a different flow's code. Step 1 already established the target flow, so you have the id. **Once per flow.** The body it returns is still in your context, and it is the largest single payload in this workflow — re-fetching the same flow re-adds it, and every request from then on carries both copies. If an `update_datastage_flow` was rejected, the flow is unchanged, so the code you already hold is still current: fix *that* text against the error and resubmit. Fetch a second time only after an edit actually landed and you need the new canonical body.
2. Splice your change into the **complete** SDK body, reusing the variable names already defined there. Never submit a fragment: the flattened SDK grammar has no way to fetch existing elements, so `flow.stages["x"]` / `link.schema` are rejected.
3. `update_datastage_flow` with the whole edited body. Bundle every change into one submission — successive submissions overwrite each other.

Use `recommend_datastage_stages` and `datastage_property_lookup` for exact stage types, property names, and enum values. Never guess them.

## Exit → VALIDATE

A flow asset now exists. Surface the returned `flow_link` to the user as a clickable link.

Both stable backends compile as part of authoring, so VALIDATE is usually a no-op confirmation. The one case that matters: if the authoring call came back with `status: "compile_error"`, the flow **was still saved** — go to VALIDATE, which routes you straight back here to fix it in place on the same `flow_id`. Never create a new flow or delete the broken one in response to a compile error.
