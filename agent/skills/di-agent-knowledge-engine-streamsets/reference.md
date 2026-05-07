# StreamSets Technical Reference

## System Requirements

### Engine Workstation

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **Operating System** | Any Linux distribution | Ubuntu 20.04+, RHEL 8+, or CentOS 8+ |
| **CPU Cores** | 2 | 4+ for production |
| **RAM** | 4 GB | 8 GB+ for production |
| **Disk Space** | 6 GB | 20 GB+ for logs |
| **Network** | Outbound HTTPS | Low-latency to data sources |

> **Important**: Do not use NFS or NAS for Data Collector files.

### Container Management

- Docker 20.10+ or Podman 3.0+
- Resources allocated via VPCs (default: 4 VPCs per engine)

## Engine Versions

### Version Support

| Version | Communication | Failover | Status Monitoring |
|---------|--------------|----------|-------------------|
| **7.1.0-0115+** | Tunneling (default) or Direct | ✓ | ✓ |
| **7.1.0** | Direct only | ✓ | ✓ |
| **6.4.x** | Direct only | ✓ | ✓ |
| **6.3.x** | Direct only | ✗ | ✗ |

### Version Selection

- **Latest version**: Recommended for new environments
- **Specific version**: Use when compatibility with existing flows is required
- **Regional availability**: Some versions may not be available in all regions

## Configuration Properties

### Data Collector Engine Properties

Advanced properties for custom keystore, credential stores, email executors, and custom stage development. Uses Java properties file format.

Example: `https.keystore.path=/path/to/keystore.jks`

### Log4j2 Properties

Configure logging levels, file sizes, and retention.

Example: `logger.sdc.level=DEBUG`, `appender.rolling.policies.size.size=500MB`

### JVM Options

Java Virtual Machine configuration.

Common: `-Xmx4096m` (heap size), `-Xlog:gc*:file=/logs/gc.log` (GC logging), `-Duser.timezone=UTC`

### Environment Variables

Custom variables for the engine container. Cannot override `SSET_PROJECT_ID`, `SSET_BASE_URL`, `SSET_API_KEY`.

### Docker/Podman Command Options

Additional container run options: `--mount` (volumes), `--hostname` (direct communication), `--dns` (custom DNS). Cannot use `--cpus` (set via VPCs).

## Network Requirements

### Firewall Access

Engine workstations require outbound access to:

#### IBM watsonx.data Integration

| Service | Protocol | Port | Purpose |
|---------|----------|------|---------|
| Control Plane | HTTPS | 443 | Engine registration and control |
| Tunneling Service | WSS | 443 | Tunneling communication (7.1.0-0115+) |

#### Data Sources and Targets

Configure firewall rules based on your specific data sources and targets:

| System Type | Typical Ports |
|-------------|---------------|
| **Databases** | PostgreSQL (5432), MySQL (3306), Oracle (1521), SQL Server (1433) |
| **Message Queues** | Kafka (9092), RabbitMQ (5672), ActiveMQ (61616) |
| **Cloud Storage** | S3 (443), Azure Blob (443), GCS (443) |
| **APIs** | HTTP (80), HTTPS (443) |

### Network Performance

- **Latency**: < 100ms to watsonx, < 50ms to sources/targets for high-throughput
- **Bandwidth**: 10 Mbps minimum, 100+ Mbps recommended, 1+ Gbps for large volumes

## Resource Thresholds

### Default Thresholds (Engine 6.4+)

| Threshold | Default | Range | Impact |
|-----------|---------|-------|--------|
| **Max CPU Load** | 80% | 1-100% | New jobs rejected when exceeded |
| **Max Memory Used** | 100% | 1-100% | New jobs rejected when exceeded |
| **Max Jobs Running** | 10 | 1-100 | New jobs rejected when reached |

### Threshold Behavior

When an engine reaches a threshold:
1. Engine continues running existing jobs
2. New jobs are not assigned to this engine
3. Jobs start on other available engines
4. Engine accepts jobs again when below threshold

### Tuning Recommendations

**CPU threshold**:
- Lower (60-70%) for consistent performance
- Higher (80-90%) for maximum utilization

**Memory threshold**:
- Keep at 100% to use all available memory
- Lower (80-90%) if experiencing out-of-memory errors

**Max jobs**:
- Lower for resource-intensive jobs
- Higher for lightweight jobs
- Monitor actual resource usage to optimize

## Sources with Offset Support

Sources that maintain offsets can safely use multiple-engine environments with job failover.

### Sources That Maintain Offsets

**File-based**:
- Directory (with file tracking)
- SFTP/FTP Client
- Amazon S3
- Azure Data Lake Storage
- Google Cloud Storage

**Database**:
- JDBC Consumer (with offset column)
- Oracle CDC Client
- SQL Server CDC Client
- MySQL Binary Log
- PostgreSQL WAL

**Message Queues**:
- Kafka Consumer
- Kafka Multitopic Consumer
- Amazon SQS Consumer
- Azure Event Hub Consumer
- Google Pub/Sub Subscriber

**APIs**:
- HTTP Client (with pagination)
- REST Service (with offset tracking)

### Sources Without Offset Support

Use single-engine environments for these sources:

- Directory (without file tracking)
- HTTP Server (listening mode)
- WebSocket Server
- TCP Server
- UDP Source
- Dev Data Generator (random data)


## API Endpoints

### Engine Health Check

**Direct communication only**: `/public-rest/is-running` endpoint returns "Engine is running" when accessible.

### Engine Metrics

Access engine metrics through the watsonx.data integration UI:
- Navigate to environment details
- View engine status and health
- Monitor resource usage (6.4+)

## Troubleshooting

### Common Issues

#### Engine Won't Start

**Symptom**: Container exits immediately after starting

**Possible causes**:
- Invalid API key
- Network connectivity issues
- Port conflicts (18630)
- Insufficient resources

**Diagnostic steps**:
- Check container logs for errors
- Verify API key is set correctly
- Check if port 18630 is available
- Verify system has adequate resources

#### Engine Shows "Lost" Status

**Symptom**: Engine status shows "Lost" in environment details

**Possible causes**:
- Engine crashed
- Network outage
- Workstation shutdown
- Resource exhaustion

**Diagnostic steps**:
- Verify container is running
- Check container logs for errors
- Check system resources (CPU, memory, disk)
- Verify network connectivity to watsonx

#### Jobs Not Starting

**Symptom**: Jobs remain in queue, don't start

**Possible causes**:
- All engines at resource thresholds
- No engines online
- Missing task credentials
- Environment configuration issues

**Diagnostic steps**:
1. Check engine status in environment details
2. Verify resource thresholds not exceeded
3. Confirm task credentials exist
4. Review engine logs for errors

#### Poor Performance

**Symptom**: Low throughput, high latency

**Possible causes**:
- Insufficient resources
- Network latency
- Inefficient flow design
- Source/target bottlenecks

**Diagnostic steps**:
- Monitor container resource usage
- Test network latency to sources and targets
- Review engine logs for warnings
- Analyze job metrics in watsonx UI

### Log Locations

- **Engine log file**: `/logs/sdc.log` within container
- **Container stdout/stderr**: Available via standard container log commands
- **Garbage collection logs**: `/logs/gc.log` (if enabled via JVM options)

## Best Practices Summary

### Security

- Rotate API keys regularly
- Use custom CA certificates for self-signed systems
- Enable credential stores for sensitive data
- Restrict network access to required systems only

### Performance

- Allocate adequate VPCs for workload
- Monitor resource usage and adjust thresholds
- Use multiple engines for high-throughput workloads
- Optimize flow design for efficiency

### Reliability

- Deploy multiple engines for production
- Verify source stages maintain offsets
- Configure source systems for resiliency
- Monitor engine health regularly

### Maintenance

- Keep engines on latest version
- Clean up unused containers and images
- Review logs for warnings and errors
- Plan updates during maintenance windows

### Monitoring

- Check engine status daily
- Monitor resource usage trends
- Set up alerts for Lost engine status
- Review job performance metrics