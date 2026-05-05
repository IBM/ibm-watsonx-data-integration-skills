---
name: streaming-streamsets-engine
description: Q&A reference for StreamSets Data Collector engines and environments — environment configuration, engine deployment, job execution, communication methods (tunneling/direct), high availability, failover, monitoring, and resource management. Use for StreamSets infrastructure, engine operations, and job lifecycle questions.
---

# StreamSets Engine

## When to Use StreamSets

- Real-time and batch data integration
- Continuous data processing and streaming
- Cloud and on-premises data movement
- Building data pipelines with visual flow designer
- Integration with modern data platforms and APIs
- Change data capture (CDC) operations

## Engine Characteristics

- **Container-based**: Runs as Docker/Podman containers in your network
- **Data ownership**: All processing occurs within your infrastructure
- **Continuous processing**: Jobs run continuously, processing data as it arrives
- **High availability**: Multiple engines support failover and load distribution
- **Flexible communication**: Tunneling (default) or direct connection methods

## Key Concepts

- **Environments**: Configure engines and compute resources for projects
- **Engines**: Data Collector containers that execute flows
- **Jobs**: Flow executions that run continuously on engines
- **Offsets**: Track processing progress for resumable execution
- **VPCs**: Virtual CPUs allocated to engine containers

## Architecture

- **Browser** ↔ **watsonx.data integration** ↔ **Engine** (in your network)
- Engines process data locally, send metrics to watsonx.data integration
- Jobs fail over automatically between engines (6.4+)
- Resource thresholds prevent engine overload

## Quick Start

1. **Create environment** → [environments.md](./environments.md#creating-an-environment)
2. **Run engine** → [engines.md](./engines.md#running-an-engine)
3. **Execute job** → [jobs.md](./jobs.md#running-a-job)

## References

- [Environments](environments.md) - Environment creation and configuration
- [Engines](engines.md) - Engine deployment, management, and monitoring
- [Jobs](jobs.md) - Job execution and lifecycle management
- [Technical Reference](reference.md) - System requirements, commands, and troubleshooting