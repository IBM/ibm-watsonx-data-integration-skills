# StreamSets Environments

## Overview

A StreamSets environment configures Data Collector engines and compute resources for your flows and jobs. Each environment runs engines in your corporate network and can support multiple engines for increased capacity.

## Creating an Environment

### Access Environment Creation

1. Navigate to the **Manage** tab of your project
2. Click the **StreamSets** tool
3. Click **New environment**

### Basic Configuration

| Property | Description |
|----------|-------------|
| **Name** | Unique identifier for the environment |
| **Description** | Optional description of the environment's purpose |
| **Data Collector Engine Version** | Engine version to run (use latest for newest features) |

> **Note**: Some engine versions may not be available in all regions or cloud platforms.

### Configure Details

#### Stage Libraries

Stage libraries determine which stages (sources, targets, processors) are available in your flows.

- **Default libraries**: Sufficient for getting started
- **Custom selection**: Click "Select stage libraries" to add more

#### External Resources

Optional archive file (TGZ or compressed format) containing external resources used by the engine. Must be:
- Imported as a data asset in your project
- Using the required directory structure

#### VPCs Allocated to Engine

Number of virtual CPUs allocated to the engine container.

- **Default**: 4 VPCs (suitable for most streaming use cases)
- **Impact**: Determines your StreamSets compute resource usage

### Resource Thresholds

Configure when engines stop accepting new jobs:

| Threshold | Default | Description | Version |
|-----------|---------|-------------|---------|
| **Max CPU Load** | 80% | Maximum CPU usage before rejecting new jobs | 6.4+ |
| **Max Memory Used** | 100% | Maximum Java heap usage before rejecting new jobs | 6.4+ |
| **Max Jobs Running** | 10 | Maximum concurrent jobs per engine | 6.4+ |

### Advanced Configuration

Expand the **Advanced configuration** section to customize:

- **Data Collector Engine Properties**: Custom keystore, credential stores, email executors, custom stages
- **Log4j2 Properties**: Logging levels and configurations
- **JVM Options**: Java Virtual Machine settings
- **Environment Variables**: Custom variables (cannot override `SSET_PROJECT_ID`, `SSET_BASE_URL`)
- **Docker Command Options**: `--mount` (volumes), `--hostname` (direct communication). Cannot use `--cpus` (set via VPCs)
- **Custom CA Certificate**: For systems using self-signed certificates

### Finalize Creation

1. Click **Save**
2. Complete the listed prerequisites
3. Copy and run the engine command to deploy an engine

## Engine Communication Methods

Your browser communicates with engines using one of two methods:

### Tunneling (Default)

**Supported**: Engine version 7.1.0-0115 and later

**How it works**:
- Browser connects to watsonx.data integration
- Watsonx.data integration acts as encrypted proxy to engine
- Data is encrypted in transit but passes through watsonx.data integration

**Advantages**:
- No additional setup required
- Secure by default

**Considerations**:
- Preview data passes through watsonx.data integration
- Data is encrypted but leaves corporate network temporarily

### Direct Communication

**Supported**: All engine versions

**How it works**:
- Browser connects directly to engine over HTTPS
- All data stays within corporate network

**Advantages**:
- Preview data never leaves corporate network
- Full data isolation

**Requirements**:
- Additional network configuration
- Engine must be accessible from browser
- Valid hostname configuration

## Customizing the Engine Command

Customize the engine run command via environment's advanced configuration for environment variables, volume mounts, hostname overrides, or Docker/Podman options.

**Process**: Stop engines → Edit environment → Update advanced configuration → Save → Run updated command

> **Warning**: Incorrect configuration can cause startup failures.

## Configuring Environments

Modify configuration to add stage libraries, external resources, or advanced settings (custom certificates, credential stores, email executors, custom stages).

**Process**: Environment details → Edit environment → Update configuration → Save → Restart engines

## Best Practices

### Environment Naming

Use descriptive names that indicate:
- Project or team
- Purpose (dev, test, prod)
- Data source or use case

Example: `sales-team-prod-postgres`

### Version Management

- Use latest engine version for new environments
- Test new versions in non-production environments first
- Plan upgrades during maintenance windows

### Resource Allocation

- Start with default 4 VPCs
- Monitor resource usage
- Scale up VPCs if jobs frequently wait for resources
- Consider multiple engines before increasing VPCs

### Multiple Environments

Create separate environments for:
- Different projects or teams
- Development vs. production workloads
- Different engine versions
- Isolated testing