# Data Collector Engines

## Overview

Data Collector engines run as containers on workstations in your corporate network. Each engine processes data according to flow configurations, maintaining data ownership and control within your infrastructure.

## Prerequisites

Complete prerequisites once for your account, and on each workstation where you'll run an engine.

### Account Prerequisites

Complete these steps once per IBM watsonx account. Reuse the API keys for all environments and engines.

#### 1. Create Task Credentials (User API Key)

Task credentials enable secure authorization for long-running data integration tasks.

**Purpose**: Authenticate StreamSets jobs
**Storage**: Securely stored in Vault
**Scope**: Reusable across all jobs

See: [Creating task credentials for jobs](https://www.ibm.com/docs/en/watsonx/data-integration)

#### 2. Create Cloud Account API Key

Required for engine authorization when running the engine command.

**IBM Cloud**:
1. Navigate to **Administration** > **Access (IAM)**
2. Select **API keys**
3. Click **Create**
4. Save or download the API key value

**AWS**:
1. Navigate to **Administration** > **Access (IAM)** > **Personal API keys**
2. Click **Create**
3. Save or download the API key value

### Engine Workstation Prerequisites

Complete on every workstation where you plan to run an engine.

#### System Requirements

| Component | Minimum Requirement |
|-----------|-------------------|
| **Operating System** | Any Linux distribution |
| **CPU Cores** | 2 |
| **RAM** | 4 GB |
| **Disk Space** | 6 GB |

> **Warning**: Do not use NFS or NAS to store Data Collector files.

#### Container Management System

Install Docker or Podman on the engine workstation.

**Docker**: [Install Docker](https://docs.docker.com/get-docker/)
**Podman**: [Install Podman](https://podman.io/getting-started/installation)

#### Firewall Configuration

If the workstation is behind a firewall, configure outbound access to required systems.

See: [Firewall access for StreamSets](#firewall-requirements)

## Running an Engine

### Communication Methods

The procedure depends on your engine version and communication method:

| Engine Version | Communication Method | Procedure |
|---------------|---------------------|-----------|
| **7.1.0-0115 and later** | Tunneling (default) | [Tunneling procedure](#tunneling-communication) |
| **7.1.0-0115 and later** | Direct | [Direct procedure](#direct-communication) |
| **7.1.0 and earlier** | Direct | [Direct procedure](#direct-communication) |

### Tunneling Communication

**Supported**: Engine version 7.1.0-0115 and later (default method)

#### How It Works

- Browser connects to watsonx.data integration
- Watsonx.data integration proxies encrypted traffic to engine
- No additional network configuration required

#### Steps

1. **Export API Key**

   In a UNIX shell (e.g., Bash):
   ```bash
   export SSET_API_KEY=<your_api_key>
   ```

2. **Retrieve Engine Command**

   - Navigate to **Manage** > **StreamSets** tool
   - Click environment **Options** > **Get run command**
   - Click **Copy to Clipboard**

3. **Modify Command (if using Podman)**

   Change `docker` to `podman` in the command.

4. **Run Engine Command**

   Paste and execute the command in your terminal.

5. **Verify Startup**

   The command prompt displays the engine container ID when successful.

### Direct Communication

**Supported**: All engine versions

#### How It Works

- Browser connects directly to engine over HTTPS
- All data stays within corporate network
- Requires valid hostname configuration

#### Steps

1. **Export API Key**

   ```bash
   export SSET_API_KEY=<your_api_key>
   ```

2. **Verify Hostname**

   ```bash
   echo $(hostname)
   ```

   If this doesn't return a valid hostname, you'll need to customize the engine command.

3. **Retrieve Engine Command**

   - Navigate to **Manage** > **StreamSets** tool
   - Click environment **Options** > **Get run command**
   - Click **Copy to Clipboard**

4. **Modify Command**

   Make these changes as needed:
   
   - **For Podman**: Change `docker` to `podman`
   - **For invalid hostname**: Replace `$(hostname)` with actual hostname
     ```bash
     --hostname "localhost" \
     ```
     
     Or use the specific workstation hostname.

5. **Run Engine Command**

   Execute the modified command.

6. **View Container Logs**

   ```bash
   docker logs <container_id>
   # or
   podman logs <container_id>
   ```

   The logs display the engine URL.

7. **Verify Engine Accessibility**

   Access the engine URL from logs with `/public-rest/is-running` endpoint to confirm the engine is running.

## Running Multiple Engines

Deploy multiple engines for a single environment to:
- Increase processing capacity
- Support job failover and high availability

### How It Works

- Each additional engine increases processing capacity
- Jobs start on any online engine within resource thresholds
- Job assignment is arbitrary when multiple engines are available
- Jobs automatically fail over to another engine if one shuts down unexpectedly

### Deployment

1. Set up additional workstation with engine prerequisites
2. Run the same engine command on the new workstation
3. Repeat for each additional engine

> **Note**: Number of engines affects StreamSets compute usage.

### Job Failover (Engine 6.4+)

When an engine becomes unavailable, jobs automatically restart on another available engine.

#### Failover Behavior

- Job continues from last-saved offset
- Maximum 3 failover attempts per job
- After 3 failures, job run fails
- Some data may be reprocessed if engine stopped mid-batch

#### Failover Guidelines

**✓ Verify Source Stages Maintain Offsets**

Most sources save offsets during processing. Jobs with these sources can safely use multiple engines.

Sources that don't maintain offsets will reprocess from the beginning, causing duplicates. Use single-engine environments for these jobs.

See: [Sources that maintain offsets](#sources-with-offset-support)

**✓ Ensure All Engines Can Access Systems**

All engines must be able to access source and target systems.

**Good**: External systems (databases, Elasticsearch) - any engine can continue processing
**Bad**: Local directories on specific workstations - other engines cannot access

**✓ Configure Source System Resiliency**

Job failover provides processing high availability, not data ingestion high availability.

For sources that receive requests (HTTP Server, WebSocket Server):
- Configure clients to retry on errors
- Set up load balancing to redirect to remaining engines during failover

## Monitoring Engines

### Viewing Engine Health

Navigate to **Manage** > **StreamSets** > Environment name

**Engine Health Summary** (6.4+):
- Format: `<online_engines>/<total_engines>`
- Example: `2/3` means 2 of 3 engines are online

### Engine Status (6.4+)

| Status | Description |
|--------|-------------|
| **Online** | Running and available for jobs |
| **Offline** | Gracefully stopped |
| **Starting** | Engine is starting up |
| **Lost** | Not responding (unexpected shutdown or network issue) |
| **Not Available** | Status unavailable (rare) |
| **Not Supported** | Engine version doesn't support status reporting |

### Viewing Engine Logs

Engine logs are available at `/logs/sdc.log` within the container, or via standard container log commands.

## Managing Engines

### Freeing Disk Space

Container management systems can accumulate unused objects. Use standard container pruning commands to remove stopped containers, unused images, and volumes.

### Deleting an Engine

Delete an engine to temporarily stop using it while retaining configuration.

#### Steps

1. **Stop all jobs** running on the engine
2. **Stop and remove the container** using standard container commands
3. **Delete from environment**:
   - Navigate to **Manage** > **StreamSets** > Environment name
   - Click **Delete** for the engine

To redeploy later, retrieve and run the engine command again.

### Deleting an Environment

Delete an environment when you no longer need the engines or configuration.

#### Steps

1. **Stop all jobs** on all engines
2. **Stop and remove all engine containers** using standard container commands
3. **Delete all engines from environment**:
   - Navigate to **Manage** > **StreamSets** > Environment name
   - Click **Delete** for each engine
4. **Delete environment**:
   - Close environment details
   - Click environment **Options** > **Delete environment**
   - Confirm deletion

## Best Practices

### Engine Deployment

- **Development**: Single engine per environment
- **Production**: Multiple engines for high availability
- **Testing**: Separate environment from production

### Monitoring

- Check engine status regularly
- Monitor disk space on workstations
- Review engine logs for errors or warnings
- Set up alerts for Lost engine status

### Maintenance

- Plan engine updates during low-traffic periods
- Test new engine versions in non-production first
- Keep engines on same version within an environment
- Clean up unused containers and images regularly

### High Availability

- Deploy at least 2 engines for production workloads
- Ensure all engines can access required systems
- Verify source stages maintain offsets
- Configure source systems for resiliency
- Monitor failover events and investigate causes