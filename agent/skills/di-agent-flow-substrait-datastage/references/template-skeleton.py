# ibm-watsonx-data-integration SDK script skeleton for di-agent-flow-substrait-datastage.
# Reference: https://ibm.github.io/ibm-watsonx-data-integration-sdk/index.html
#
# Generation contract:
#   - The agent MUST NOT rewrite anything outside the `<<< BEGIN_FILL >>>` /
#     `<<< END_FILL >>>` block inside create_flow(). Everything else
#     (imports, ExitCode, module-level platform/project init, create_flow
#     scaffolding, run_flow, monitor_job, main) is fixed boilerplate.
#   - The agent fills the BEGIN_FILL block with the three labeled sections
#     "# Stage definition", "# Flow graph", "# Schema definition" — in that
#     order — derived from the optimized full-pushdown Substrait plan.
#   - The agent substitutes `<FLOW_NAME>` and `<PROJECT_ID>` in the surrounding
#     boilerplate. No other placeholders exist outside the fill block.
#   - This skeleton is meant to be saved and run as a complete Python script for
#     local fallback. When MCP create_datastage_flow (or update_datastage_flow,
#     for revising an existing flow) is available, derive a separate no-boilerplate
#     SDK subset from the fill block; do not submit this full script to the MCP tool.
#
# Placeholders used INSIDE the BEGIN_FILL block (when filling):
#   <CONN_NAME>          DataStage connection name (project.connections.get(name=...))
#   <CONNECTOR_LABEL>    connector label from references/datastage-connector-sdk-reference.md
#   <CONNECTOR_VAR>      <SDK class / map name>_0 from the same lookup (e.g. postgresql_ibmcloud_0)
#   <CONNECTOR_ENUM>     enum class from references/datastage-connector-sdk-reference.md
#   <SQL_STATEMENT>      rendered sqlStatement from the read node's enhancement
#   <PARAMETER_SETUP>    optional local parameter declarations and parameter-set
#                        attachments emitted before any stage definitions
#   <OUTPUT_FILE>        CSV output path for the Sequential file sink
#   <SCHEMA_FIELDS>      one schema_<CONNECTOR_VAR>.add_field(...) per output column

from ibm_watsonx_data_integration.common.auth import BearerTokenAuthenticator, IAMAuthenticator
from ibm_watsonx_data_integration import Platform
from ibm_watsonx_data_integration.services.datastage import *
from ibm_watsonx_data_integration.services.datastage.models.enums import *
from ibm_watsonx_data_integration.cpd_models.project_model import Project
from ibm_watsonx_data_integration.cpd_models.connections_model import Connection
from ibm_watsonx_data_integration.cpd_models.job_model import JobRunState, Job, JobRun

from typing import cast
from pathlib import Path
from enum import IntEnum

import os
import sys
import time
import argparse

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(*args, **kwargs):
        return False


FLOW_NAME = "<FLOW_NAME>"
PROJECT_ID = "<PROJECT_ID>"


class ExitCode(IntEnum):
    """Exit codes for the DataStage flow script

    Ranges:
        0: Success
        10-19: Flow creation errors
        20-29: Job run errors
        30-39: Job monitoring errors
    """
    SUCCESS = 0
    FLOW_CREATION_FAILED = 10
    JOB_RUN_START_FAILED = 21
    NO_JOB_RUNS_FOUND = 31
    JOB_EXECUTION_FAILED = 32
    JOB_MONITORING_ERROR = 33


base_dir = Path(__file__).parent
load_dotenv(dotenv_path=base_dir / "credentials.env")

api_key = os.environ.get("API_KEY") or os.environ.get("WATSONX_API_KEY")
bearer_token = os.environ.get("BEARER_TOKEN") or os.environ.get("DE_MCP_BEARER_TOKEN")
base_auth_url = os.environ.get("BASE_AUTH_URL") or os.environ.get("IAM_URL")
base_api_url = os.environ.get("BASE_API_URL") or os.environ.get("GATEWAY_URL")
project_id = os.environ.get("PROJECT_ID") or os.environ.get("WATSONX_PROJECT_ID") or PROJECT_ID

if not base_api_url:
    raise RuntimeError("Set BASE_API_URL or GATEWAY_URL.")

if api_key:
    auth = IAMAuthenticator(api_key=api_key, base_auth_url=base_auth_url)
elif bearer_token:
    auth = BearerTokenAuthenticator(bearer_token=bearer_token)
else:
    raise RuntimeError("Set API_KEY/WATSONX_API_KEY or BEARER_TOKEN/DE_MCP_BEARER_TOKEN.")

platform = Platform(auth, base_api_url=base_api_url, base_url=base_auth_url)
project = cast(Project, platform.projects.get(project_id=project_id))


def create_flow():
    """Create or recreate and update/compile the DataStage flow

    Returns:
        int: Exit code (ExitCode.SUCCESS or ExitCode.FLOW_CREATION_FAILED)
    """
    try:
        flow = cast(BatchFlow, project.flows.get(flow_type="batch", name=FLOW_NAME))
        print(f"Found existing flow {FLOW_NAME}. Deleting to recreate.")
        project.delete_flow(cast(BatchFlow, flow))
    except Exception:
        print(f"Flow {FLOW_NAME} not found. Creating a new one.")

    try:
        print(f"Creating flow: {FLOW_NAME}")
        flow = cast(BatchFlow, project.create_flow(name=FLOW_NAME, description="", environment=None, flow_type="batch"))

        # <<< BEGIN_FILL >>>
        # Fill this region with three labeled sections, in order:
        #
        #   # Stage definition
        #     - If the optimized plan contains parameters, start this section with
        #       the required flow.add_local_parameter(...) calls and any
        #       project.parameter_sets.get(...), flow.use_parameter_set(...), and
        #       runtime value calls:
        #       flow.set_runtime_value_set(...),
        #       flow.set_runtime_parameter_value(...), and
        #       flow.set_runtime_local_parameter(...). Render SQL placeholders to
        #       DataStage #PARAM# / #PARAM_SET.PARAM# syntax before assigning SQL
        #       to connector properties.
        #     - Always add the local environment parameter when parameterized SQL
        #       is emitted:
        #       flow.add_local_parameter("string", "$APT_OSL_PARAM_ESC_SQUOTE", value="True")
        #     - One database connector source in SQL mode (read_method + select_statement).
        #     - One Sequential file sink (type = "Sequential file") with these defaults:
        #       file_update_mode=SEQUENTIALFILE.AppendOverwrite.overwrite,
        #       final_delimiter=SEQUENTIALFILE.FinalDelimiter.end, file=[...],
        #       first_line_is_column_names=SEQUENTIALFILE.FirstLineColumnNames.true,
        #       delimiter=SEQUENTIALFILE.Delimiter.comma, null_field_value="NULL".
        #       delimiter/final_delimiter are enum-typed — pass the enum members,
        #       not quoted strings like "'|'"/"'end'", which the validator rejects.
        #       Always set create_data_asset=True and data_asset_name="<flow_name>"
        #       so the output file is registered as a project data asset and the
        #       result rows can be read back via read_file_data_asset.
        #
        #   # Flow graph
        #     - Exactly one link from the source to the sink, as separate statements
        #       (the chained .set_name(...).create_schema() form is rejected):
        #       link_1 = <CONNECTOR_VAR>.connect_output_to(sequentialfile_0)
        #       link_1.name = "Link_1"
        #       schema_<CONNECTOR_VAR> = link_1.create_schema()
        #
        #   # Schema definition
        #     - One schema_<CONNECTOR_VAR>.add_field(...) per output column,
        #       in the order given by relations[0].root.names. Use the canonical
        #       checked/repaired names from the optimized plan. If names are not
        #       DataStage-safe, sanitize SQL SELECT-list aliases and the output
        #       schema names before filling this block. Types come from
        #       read.baseSchema.struct.types in the same positional order.
        #       Signature is add_field("<DATASTAGE_TYPE>", "<name>", ...): the
        #       DataStage type is the FIRST positional arg, the column name the
        #       SECOND — e.g. add_field("BIGINT", "LOADED_ROW_COUNT", nullable=True).
        #       Passing the name first fails validation. Optional kwargs supported
        #       by the installed SDK: nullable=True, length=1024, precision=, scale=.
        #
        # Do not insert additional stages, transformers, joins, or alternate sinks.
        # <<< END_FILL >>>

        project.update_flow(flow)
        print(f"Flow {FLOW_NAME} created and updated/compiled successfully.")
        return ExitCode.SUCCESS
    except Exception as e:
        print(f"Failed to create flow: {e}", file=sys.stderr)
        return ExitCode.FLOW_CREATION_FAILED


def run_flow(flow_name=None):
    """Start a job run for the flow

    Args:
        flow_name: Optional flow name to use. If not provided, uses FLOW_NAME

    Returns:
        tuple: (job, run) on success, (None, None) on failure
    """
    if flow_name is None:
        flow_name = FLOW_NAME

    job_name = f"{flow_name}.DI"

    try:
        try:
            job = cast(Job, project.jobs.get(name=job_name))
            print(f"Using existing job: {job_name} (ID: {job.job_id})")
        except Exception:
            print(f"Creating job: {job_name}")
            flow = cast(BatchFlow, project.flows.get(flow_type="batch", name=flow_name))
            job = cast(Job, project.create_job(flow=flow, name=job_name))

        print(f"Starting job run for: {job.job_id}")
        run = cast(JobRun, job.start(name=job_name, description=f"Run for flow {flow_name}"))
        print(f"Job started. Run ID: {run.job_run_id}")

        return job, run
    except Exception as e:
        print(f"Failed to start job run: {e}", file=sys.stderr)
        return None, None


def monitor_job(job=None, run=None, flow_name=None, poll_interval=4):
    """Monitor the job run until completion

    Args:
        job: Job object (optional if flow_name provided)
        run: JobRun object (optional, will get latest if not provided)
        flow_name: Flow name to derive job name (optional)
        poll_interval: Seconds to wait between status checks (default: 4)

    Returns:
        int: Exit code (ExitCode.SUCCESS, NO_JOB_RUNS_FOUND, JOB_EXECUTION_FAILED, or JOB_MONITORING_ERROR)
    """
    # Get job if not provided
    if job is None:
        if flow_name:
            job_name = f"{flow_name}.DI"
        else:
            job_name = f"{FLOW_NAME}.DI"
        print(f"Retrieving job from project. Job name: {job_name}")
        job = cast(Job, project.jobs.get(name=job_name))

    # Get run if not provided - get the latest run
    if run is None:
        try:
            print(f"Retrieving latest job run from project...")
            runs = list(job.job_runs)
            if runs:
                run = runs[0]  # Get most recent run
                print(f"Monitoring the latest job run: {run.job_run_id} (polling every {poll_interval} seconds)")
            else:
                print("No job runs found to monitor.", file=sys.stderr)
                return ExitCode.NO_JOB_RUNS_FOUND
        except (TypeError, AttributeError):
            print("Cannot retrieve job runs. Please provide run object or start a new job first.", file=sys.stderr)
            return ExitCode.NO_JOB_RUNS_FOUND
    else:
        print(f"Using provided job and run objects")
        print(f"Monitoring the current job run: {run.job_run_id} (polling every {poll_interval} seconds)")

    states = [
        JobRunState.Completed,
        JobRunState.Failed,
        JobRunState.Canceled,
        JobRunState.CompletedWithErrors,
        JobRunState.CompletedWithWarnings
    ]

    while True:
        time.sleep(poll_interval)
        try:
            run = cast(JobRun, job.job_runs.get(job_run_id=run.job_run_id))
            status = run.state
            print(f"Current job status: {status}")
            if status in states:
                # Print logs for all terminal states
                try:
                    logs = run.logs
                    print("\n=== Job Logs ===")
                    for log in logs:
                        print(log)
                    print("=== End of Logs ===\n")
                except Exception as e:
                    print(f"Could not fetch logs: {e}", file=sys.stderr)

                if status in [JobRunState.Completed, JobRunState.CompletedWithWarnings]:
                    print("Job run finished successfully.")
                    return ExitCode.SUCCESS
                else:
                    print(f"Job run failed, status: {status}.", file=sys.stderr)
                    return ExitCode.JOB_EXECUTION_FAILED

        except Exception as e:
            print(f"Error while monitoring job: {e}", file=sys.stderr)
            return ExitCode.JOB_MONITORING_ERROR


def main():
    """Main function to handle command-line arguments

    Exit Codes:
        0: Success
        10: Flow creation failed
        21: Job run start failed
        31: No job runs found to monitor
        32: Job execution failed
        33: Job monitoring error
    """
    parser = argparse.ArgumentParser(description=f"DataStage Flow: {FLOW_NAME}")
    parser.add_argument('--create_flow', action='store_true',
                        help='Create or recreate the flow (executes until project.update_flow)')
    parser.add_argument('--run_flow', action='store_true',
                        help='Start a job run for the flow')
    parser.add_argument('--monitor_job', action='store_true',
                        help='Monitor the job run until completion')
    parser.add_argument('--flow_name', type=str,
                        help='Flow name to use (for run_flow and monitor_job)')
    parser.add_argument('--poll_interval', type=int, default=4,
                        help='Polling interval in seconds for job monitoring (default: 4)')

    args = parser.parse_args()

    # If no arguments provided, execute all steps
    if not (args.create_flow or args.run_flow or args.monitor_job):
        args.create_flow = True
        args.run_flow = True
        args.monitor_job = True

    exit_code = 0
    job = None
    run = None

    # Execute create_flow
    if args.create_flow:
        exit_code = create_flow()
        if exit_code != 0:
            sys.exit(exit_code)

    # Execute run_flow
    if args.run_flow:
        job, run = run_flow(flow_name=args.flow_name)
        if job is None or run is None:
            sys.exit(ExitCode.JOB_RUN_START_FAILED)

    # Execute monitor_job
    if args.monitor_job:
        exit_code = monitor_job(job=job, run=run, flow_name=args.flow_name, poll_interval=args.poll_interval)
        sys.exit(exit_code)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
