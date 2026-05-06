# StreamSets Jobs

## Overview

A StreamSets job executes a finished flow on a Data Collector engine. Jobs run continuously in your corporate network, processing data as it becomes available while maintaining full data ownership and control.

## How Jobs Work

### Execution Model

- **Location**: Jobs run on Data Collector engines in your corporate network
- **Data ownership**: All data stays within your infrastructure
- **Monitoring**: Engines send status updates and metrics to watsonx.data integration
- **Continuous processing**: Jobs run continuously, processing data as it arrives

### Job Lifecycle

1. **Create**: First run creates a job from a flow
2. **Run**: Job processes data continuously
3. **Stop**: Job notes the last-read offset
4. **Resume**: Next run continues from saved offset
5. **Reset**: Optionally reprocess all data from beginning

### Key Characteristics

- **One job per flow**: Each flow has a single associated job
- **One active run**: Only one job run can be active at a time
- **Offset management**: Jobs track progress and resume from last position
- **Automatic failover**: Jobs can fail over to another engine (6.4+)

## Prerequisites

Complete these prerequisites before running any StreamSets job.

### 1. Verify Running Engine

Ensure an administrator has:
- Created a StreamSets environment for your project
- Deployed at least one running Data Collector engine

See: [Running a Data Collector engine](./engines.md#running-an-engine)

### 2. Create Task Credentials

Task credentials (user-generated API key) enable secure authorization for long-running jobs.

**What it is**: User-generated API key stored securely in Vault
**Purpose**: Authenticates long-running data integration tasks
**Scope**: Reusable across all StreamSets jobs

See: [Creating task credentials for jobs](https://www.ibm.com/docs/en/watsonx/data-integration)

## Running a Job

You can start a job from two locations:
- Flow canvas (quick start)
- Job details (full control)

### From Flow Canvas

The **Run** icon on the flow canvas provides the quickest way to start a job.

#### First Run

When you click **Run** for the first time:
1. Job is automatically created for the flow
2. Job starts running immediately
3. Job runs on the environment selected for the flow
4. Job name follows format: `Job for <flow_name> <datetime_in_seconds>`

#### Subsequent Runs

After the initial run:
- Click **Run** to start a new job run
- Job uses the same configuration as before
- Job resumes from last-saved offset (unless reset)

#### Editing Job Configuration

After the first run, you can edit:
- Job name
- Job description
- Target environment

Navigate to job details to make these changes.

### From Job Details

After the initial job run creates a job, you can manage it from the job details page.

#### Accessing Job Details

Navigate to job details via:
- **Assets** tab > Click job name
- **Jobs** tab > Click job name

#### Starting a Job

1. Open job details
2. Click **Run job** icon
3. Job starts on the configured environment

#### Job Details Information

The job details page shows:
- Job configuration (name, description, environment)
- Run history with status and metrics
- Current run status (if active)
- Offset information
- Performance metrics

## Job Management

### Stopping a Job

1. Navigate to job details or flow canvas
2. Click **Stop** icon
3. Job completes current batch and stops
4. Offset is saved for next run

### Resetting Offsets

Reset offsets to reprocess data from the beginning.

**Use cases**:
- Reprocess historical data
- Recover from data quality issues
- Test flow changes with full dataset

**Warning**: Resetting offsets may cause duplicate data processing.

**Steps**:
1. Stop the job if running
2. Navigate to job details
3. Click **Reset offset**
4. Confirm the action
5. Start the job to begin from the beginning

### Monitoring Job Progress

**Real-time Metrics**: Records processed, throughput (records/sec), error count, runtime

**Job Status**: Running, Stopped, Failed, Finishing

**Job History**: Previous runs with timing, records processed, status, and errors

## Continuous Processing

Jobs continuously read, process, and write data in batches, saving offsets to track progress.

### Offset Management

Offsets track where a job stopped reading, enabling resumption. Saved periodically and on stop. Types vary by source: file position, database key/timestamp, message ID, API cursor.

### Delivery Guarantee

**At-least-once delivery**: Data may be reprocessed after engine failures, failovers, or network interruptions.

**Preventing duplicates**: Use idempotent operations, deduplication logic, or unique keys in targets.

## Job Failover (Engine 6.4+)

When using multiple engines, jobs automatically fail over if an engine becomes unavailable.

### Failover Behavior

- **Automatic**: No manual intervention required
- **Offset-based**: Continues from last-saved offset
- **Retry limit**: Maximum 3 failover attempts
- **Resource-aware**: Fails over to engines within resource thresholds

### Failover Scenarios

**Graceful shutdown**: Job stops cleanly, saves offset, can resume on any engine
**Unexpected failure**: Job fails over, may reprocess last batch
**Network outage**: Job waits for reconnection, then fails over if timeout exceeded

### Failover Requirements

For successful failover, ensure:
- Multiple engines running in environment
- Source stages maintain offsets
- All engines can access source and target systems
- Source systems configured for resiliency

See: [Job failover guidelines](./engines.md#job-failover-guidelines)

## Best Practices

- **Naming**: Include source, target, purpose, environment (e.g., `postgres-to-s3-customer-data-prod`)
- **Environments**: Single engine for dev, multiple for production
- **Monitoring**: Check status, errors, throughput; set up failure alerts
- **Error Handling**: Configure error records, implement retry logic, use dead letter queues
- **Performance**: Adjust batch size, use parallelism, ensure adequate VPCs, add engines for capacity
- **Maintenance**: Stop jobs before updates, test in non-production, plan downtime, monitor failovers

## Troubleshooting

- **Won't Start**: Check engine status, resource thresholds, task credentials, flow configuration
- **Fails Immediately**: Test connections, verify credentials/permissions, review engine logs
- **Poor Performance**: Increase VPCs/engines, optimize flow, check network, tune sources/targets
- **Duplicate Data**: Implement deduplication, use idempotent operations, consider single-engine for sources without offsets
- **Job Stuck**: Check for new data, verify target availability, review resources, check network