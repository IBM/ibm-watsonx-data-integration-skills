# DataStage Transformer Macros

Macros are built-in substitution tokens that are resolved at job start. They expose job and runtime metadata and can be used directly in Transformer derivation expressions, job control routines, and before-job/after-job subroutines. No function call or link prefix is needed — reference a macro by its bare name (e.g. `DSJobName`).

Other environment variables are accessed via `GetEnvironment("var_name")`.

---

## Job and Flow Macros

### DSFlowId

- **Description**: Returns the unique identifier for the flow the job is running.
- **Example value**: `c036d191-b353-422b-8c5e-8ba24aee3c5f`
- **Example**: Return the flow ID as a string: `DSFlowId`

### DSFlowName

- **Description**: Returns the name of the current flow.
- **Example value**: `macroTest`
- **Example**: Tag each row with the flow name: `DSFlowName`

### DSHostName

- **Description**: Returns the host name of the DataStage server where the job is running.
- **Example value**: `ds-px-runtime-5d5544db9c-rkn97`
- **Example**: Capture the runtime host for auditing: `DSHostName`

### DSJobController

- **Description**: Returns a string identifying the Watson Pipeline that launched the current job. If a DataStage job is run independently (not launched from a pipeline), this value is an empty string. If the parent pipeline has a `DSJobInvocationId` set, the value takes the form `<parent pipeline name>.<parent job invocation id>`; otherwise it is `<parent pipeline name>`.
- **Example**: Combine the job start date with the pipeline controller value for a unique audit key:
  `DSJobStartDate : "-" : DSJobController`

### DSJobId

- **Description**: Returns the unique identifier of the DataStage job definition.
- **Example value**: `86f85414-bd62-4483-85b0-bb0dea964096`
- **Example**: Return the job ID: `DSJobId`

### DSJobInvocationId

- **Description**: Returns the name displayed on the DataStage Jobs dashboard for this job run. The value can be set from a pipeline, at job start, or via a parameter/environment variable. When both `DSJobInvocationId` and a run name are present in a *Run DataStage job* node, `DSJobInvocationId` takes precedence. If neither is set, the default value `job run` is used.
- **Example value**: `9932a594-971e-462b-b4e2-e0f9dc3266c8`
- **Example**: Return the invocation ID: `DSJobInvocationId`

### DSJobName

- **Description**: Returns the fully qualified name of the running DataStage job.
- **Example value**: `macroTest.DataStage job`
- **Example**: Embed the job name in an output string: `DSJobName`

### DSJobRunId

- **Description**: Returns the unique identifier of the current job run instance.
- **Example value**: `225983db-a99f-436d-b8d8-a096bf60b4b9`
- **Example**: Return the job run ID: `DSJobRunId`

### DSJobStartDate

- **Description**: Returns the date on which the job started, in `YYYY-MM-DD` format.
- **Example value**: `2022-11-21`
- **Example**: Return the start date: `DSJobStartDate`

### DSJobStartTime

- **Description**: Returns the time at which the job started, in `HH:MM:SS` format.
- **Example value**: `16:37:38`
- **Example**: Return the start time: `DSJobStartTime`

### DSJobStartTimestamp

- **Description**: Returns the full timestamp at which the job started, in `YYYY-MM-DD HH:MM:SS` format.
- **Example value**: `2022-11-21 16:37:38`
- **Example**: Return the start timestamp: `DSJobStartTimestamp`

### DSJobWaveNo

- **Description**: Returns a sequence number that is incremented by 1 for each successful job run. Starts at 0 when compiled.
- **Example**: Return the wave number: `DSJobWaveNo`

---

## Project Macros

### DSProjectId

- **Description**: Returns the unique identifier of the current watsonx project.
- **Example value**: `7cae4661-f899-45f0-b2aa-449c7b8041cf`
- **Example**: Return the project ID: `DSProjectId`

### DSProjectName

- **Description**: Returns the name of the project in which the job is running.
- **Example value**: `ys1dev-new`
- **Example**: Return the project name: `DSProjectName`

---

## Stage Macros

### DSStageName

- **Description**: Returns the name of the current Transformer stage.
- **Example value**: `joincustomers`
- **Example**: Include the stage name in a log output column: `DSStageName`

---

## Environment Variables via GetEnvironment

Use `GetEnvironment("var_name")` to read the following runtime environment variables. These are resolved at job execution time via the `GetEnvironment` function.

| Variable | Description | Example value |
|---|---|---|
| `APT_JOB_ID` | The unique identifier of the DataStage job. | `86f85414-bd62-4483-85b0-bb0dea964096` |
| `APT_JOB_RUN_ID` | The unique identifier of the current job run. | `225983db-a99f-436d-b8d8-a096bf60b4b9` |
| `APT_JOB_RUN_PATH` | The file-system path for the current job run's working directory. | `/ds-storage/PXRuntime/Projects/7cae4661.../runs/225983db...` |
| `APT_PROJECT_ID` | The unique identifier of the current watsonx project. | `7cae4661-f899-45f0-b2aa-449c7b8041cf` |
| `HOSTNAME` | The host name of the DataStage PX runtime container. | `ds-px-default-ibm-datastage-px-runtime-85bbb6c4d8-fv54k` |

**Example**: Return the project ID from an environment variable:
`GetEnvironment("APT_PROJECT_ID")`
