# RECOVER state

## Entry

You need a rollback point before a risky edit, a restore after one went wrong, or cleanup of duplicate flows.

## Editing is overwrite-in-place — never delete-and-recreate

To change a flow you keep its id and overwrite it: `create_pyflow(replace_flow_id=…)` for pyflow flows, `update_datastage_flow` for SDK edits. Deleting a flow and recreating it is not an edit — it churns assets and destroys the id, and every job pointing at that flow dies with it. Precedence rule 3: a flow exists, so this is an edit.

## Backups are automatic — you do not create them

Every in-place edit (`create_pyflow(replace_flow_id=…)`, `update_datastage_flow`) snapshots the flow before changing it:

- the backup is named `"{name}Backup{YYYYMMDDHHMMSS}"` — e.g. `orders` → `ordersBackup20260723143025`. The suffix is appended, so a `snake_case` or `PascalCase` flow keeps its own style;
- **up to 5 snapshots are kept per flow**, and the **oldest is never discarded**. When the cap is reached, pruning takes from the middle, so you always have both the original and the recent history;
- the editing tool returns `backup_flow_id` / `backup_flow_name` for the one it just took, and `backups` — every surviving snapshot as `{flow_id, flow_name}`, **oldest first**;
- if the snapshot fails the edit is refused and the flow is untouched;
- **a burst of edits shares one rollback point.** A snapshot taken in the last couple of minutes is reused rather than duplicated, so a save → compile error → fix → save loop leaves one snapshot, not four, and the one it leaves is the definition from before the whole attempt. The result says which happened: `backup_created` for a fresh snapshot, `backup_reused` when it stood on an existing one. A snapshot taken for an edit that then failed outright is removed again, since the flow it copied was never changed.

## Choosing which backup to restore

**Do not reflexively take the newest one.** Each snapshot was taken *before* an edit, so the newest one is the state just before the most recent edit. If the flow broke two edits ago and has been getting "fixed" since, the newest backup is *also* broken. That is the common case when you arrive here from DIAGNOSE with "broke a previously-working flow", and taking the newest restores the bug.

**1. List the snapshots — the listing dates them for you.**

```
list_datastage_flows(project_id=…, entity_name="starts:<flow>Backup")
```

When the results contain snapshots, the listing looks up the flow's run history and annotates them:

- each snapshot gains **`taken_at`** (ISO, UTC) and **`predates_last_success`**;
- the response's **`last_successful_run`** says when the flow last worked, and what that means here.

**Pick the newest snapshot with `predates_last_success: true`** — the most recent version you have positive evidence worked. A snapshot with `predates_last_success: false` was taken after the flow had already broken, so restoring it restores the fault.

You do not need to fetch run history yourself; that comparison is what the annotation is. If it is absent — no successful run on record, or the lookup failed — fall back to reading the `YYYYMMDDHHMMSS` in each name against `list_job_runs` for the flow's job. A flow with no successful run at all never worked: that is a DIAGNOSE/AUTHOR problem, not a restore.

On StreamSets the listing tool is `list_streamsets_flows`, which has no name filter — pass `exclude_backups=False` and pick the `<flow>Backup<timestamp>` names out of the results yourself. It does not annotate them, so date them against the run history yourself.

**2. Say which one and why before restoring.** "The last clean run was Tuesday 14:02, so I'm going back to the copy saved Tuesday 09:30 rather than yesterday's." A restore discards work, so the user needs to be able to check the call.

- Nothing predates the last good run → the whole visible history is post-breakage. Prefer `backups[0].flow_id`, the oldest and always-kept, from before this editing sequence began.
- Timestamps don't separate the candidates → show the list with dates and ask.
- You have evidence the *last* edit caused it → the newest is correct.

## Scenarios

| Situation | Result |
|---|---|
| Flow created, never edited | No backup. Nothing has been overwritten yet. |
| One edit | One backup: the version before that edit. |
| Four edits, edit 3 broke it | Four backups. `backups[0]` is the original (good); the newest holds the already-broken v4. Restore `backups[0]`. |
| More than 5 edits | Five backups: the original plus the four most recent. Middle versions are dropped. |
| Edits on different days | Same rules — the timestamps tell you when each was taken. |
| Flow renamed, then edited | Older backups no longer match the new name and are orphaned; a fresh history starts. Delete orphans if you spot them. |
| You edit a backup directly | No snapshot is taken — backups are not backed up. |

So **do not call `duplicate_asset` before an edit** — the tool already did, and a manual one just leaves a second copy behind.

`duplicate_asset` is still the right tool for a *deliberate* copy: the user wants a named variant to work on, or a checkpoint they need kept beyond the rolling five. Name those something that does not end in `Backup<timestamp>`, so they are not mistaken for an automatic snapshot and cleaned up.

**Caveats on any duplicate, automatic or manual:** it does **not** copy jobs or schedules, and cross-flow (sub-flow) references are not preserved.

## Restore

Pick the right snapshot first (see "Choosing which backup to restore" above) — its id is in the `backups` list the editing tool returned, or find them with `list_datastage_flows(entity_name="starts:{name}Backup")`.

**Restore by overwriting the live flow with the snapshot's definition — do not delete anything.** A restore is just an edit whose new content happens to be an old version:

1. Read the chosen snapshot's definition: `retrieve_datastage_flow_code(flow_id=<snapshot id>)`.
2. Overwrite the broken flow **in place** with it: `update_datastage_flow(flow_name=<the broken flow's name>, project_id=…, sdk_code=<that code>)` — this tool addresses the flow by **name**, not by id — or `create_pyflow(replace_flow_id=<the broken flow's id>, …)` for a pyflow flow.

That is the whole restore. The flow keeps its id, so **its jobs and schedules stay attached**; the broken state is snapshotted automatically before the overwrite, so the restore itself is undoable; and nothing is deleted, so there is **no cascade to reason about**. Then re-run to confirm it works.

**Do not restore by deleting the broken flow and swapping a copy in.** The old delete-and-recreate dance (duplicate the snapshot → delete the broken flow → rename the copy) destroys the version history — `delete_asset` cascades to the flow's snapshots — and breaks every job pointing at the flow even when the order is right. `delete_asset` refuses it: deleting a flow that still has snapshots returns `REFUSED_FLOW_HISTORY_DELETE`. **That refusal is the answer, not an obstacle.** Do not set `deleting_version_history_on_purpose` to get past it; go back and overwrite in place. Only delete a flow when removing it is the *goal* (de-duplication below).

If jobs or schedules matter and you would rather not touch the live flow at all, point the user at the snapshot and let them choose — but the in-place overwrite already preserves those, so it is the default.

## Snapshots and clutter

Snapshots are capped at 5 per flow, and `list_datastage_flows` **hides them by default** — so an ordinary listing shows real flows only, and you do not need to clean them up as housekeeping. To see them, name them (`list_datastage_flows(entity_name="starts:<flow>Backup")`) or pass `exclude_backups=False`. When a listing hides any, it says so in `hidden_snapshots` — that is the filter working, not results being withheld, and it is not a prompt to go looking for them.

**A user calling snapshots "duplicates", "extra copies", or "clutter" is describing something they did not know existed, not asking you to delete it.** They are the only version history there is. Explain what they are and that they are capped and automatic; offer to restore one if an edit went wrong. `delete_asset` refuses them outright (`REFUSED_SNAPSHOT_DELETE`) — treat that refusal as the answer, not an obstacle to route around, and do not re-list with `exclude_backups=False` in order to delete what the default listing was protecting. If the user, having been told, still wants the history gone, deleting the flow itself takes its snapshots with it.

Deleting a flow deletes its snapshots with it (reported as `deleted_backups`). This is why a restore overwrites the live flow in place (see "Restore" above) rather than deleting it — an in-place restore never puts the version history at risk, so the delete-ordering question does not arise.

## De-duplicate

If a mis-route produced several flows for one request:

**1. Find the candidates.** `list_datastage_flows` for same-base-name variants.

**2. Establish which one is real from attachment and run history, not from the names.** Near-identical names and creation times cannot tell you which flow the user depends on:

```
list_jobs(project_id=…)                    → which candidate has a job pointing at it
list_job_runs(project_id=…, job_ids=[…])   → which of those has run, and succeeded
```

A flow with a job beats one without; among several with jobs, the one with a successful run wins. Newest-wins is a guess — the last flow a bad run produced is often the one that never worked.

**3. Say which you are keeping and on what evidence, then delete the rest.** Deleting flows is irreversible, and afterwards the user has no way to check the reasoning. A redundant flow that was itself edited has snapshots, so its deletion returns `REFUSED_FLOW_HISTORY_DELETE` — here that refusal *is* satisfiable, because removing the flow is the goal: confirm with the user, then re-call with `deleting_version_history_on_purpose=True`.

**"The rest" never includes snapshots.** De-duplication operates on the redundant *flows* a bad run produced — separate assets, each a full attempt at the same request. A `<name>Backup<timestamp>` is not one of those; it is the history of the flow you are keeping. The default listing already excludes them, so work from that listing and do not widen it to find more things to delete.

**Never delete a flow you did not create in this session without confirming with the user.**

## Exit

→ **AUTHOR** to re-apply the change, or → **RUN** if the restored flow is what the user wanted. If recovery is exhausted and the flow still cannot be made to work, that is the terminal escape: offer `di-agent-bug-report`.
