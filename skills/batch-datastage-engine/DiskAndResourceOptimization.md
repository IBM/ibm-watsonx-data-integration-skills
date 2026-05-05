# Disk and Resource Pool Optimization

## Overview
Proper disk configuration and resource pool management are critical for DataStage performance. This guide covers scratch disks, resource disks, physical hardware, and resource pool strategies.

---

## Disk and Filesystem Optimization

Proper scratch and resource disk configuration significantly affects job performance.

**Disk I/O Impact**: Reading source data, writing intermediate results, sorting/aggregation operations, writing target data

**Key Requirements**: Multiple fast local disks, dedicated to DataStage, with adequate space will result in optimal performance. 
Poor configurations include using slow disks, insufficient space, or shared disks which will lead to performance bottlenecks and slowdowns. 

---

## Scratch Disk Configuration

Scratch disks are used for temporary storage during job execution, such as sorting spill files, aggregation/join temporary files, and buffer space. 
They are typically used for high I/O operations and can be deleted after job completion. 


### Optimal Setup

**1. Multiple Scratch Disks**
- Configure multiple local SSDs per node (e.g., /scratch1, /scratch2, /scratch3)
- Benefits: Parallel I/O, distributed load, higher throughput, reduced contention
- Single disk creates serial I/O bottleneck

**2. Storage Type**
- **Local Disks**: Low latency, high throughput, predictable performance (always use)
- **Network Storage (NFS/SAN)**: Network latency, shared bandwidth, variable performance (avoid)

**3. Disk Type**
- **SSD**: Fastest, low latency, high IOPS (best for scratch)
- **SAS/SATA**: Moderate performance, acceptable if SSD unavailable
- Never use slow network storage

**4. Filesystem**
- **Linux**: ext4 (general purpose), xfs (better for large files)
- **AIX**: jfs2 (standard), Enhanced JFS2 (large files)
- Tune for large files, disable atime, optimize block size

---

## Resource Disk Configuration

Resource Disks are used for storing Data Sets, intermediate results, and persistent data between job executions. 
They are critical for job reliability and must be reliable and have sufficient space.

### Optimal Setup

**1. Separate from Scratch**
- Keep scratch and resource disks separate to avoid I/O contention
- Example: Scratch (/scratch1-3), Resource (/data1-3)

**2. Multiple Resource Disks**
- Configure multiple disks per node for parallel I/O and load distribution
- Example: /data1, /data2, /data3 for Data Sets

**3. Capacity Planning**
- Estimate data volumes + intermediate results + growth + safety margin
- Example: 500 GB daily + 200 GB intermediate × 1.5 safety = 1,050 GB per node

---

## Physical Hardware Architecture

**1. Disk Controller**
- Hardware RAID (not software) with battery-backed cache
- RAID 0 for scratch (performance), RAID 10 for resource disks (performance + reliability)
- Avoid RAID 5/6 (slow writes)

**2. Disk Layout**
- Separate physical disks for: OS, DataStage software, scratch (multiple), resource (multiple), database
- Benefits: No I/O contention, independent performance, better reliability

**3. Network Architecture (Clustered Environments)**
- High-speed interconnect (10 Gb/s+), low latency, dedicated DataStage network
- Benefits: Fast data transfer, no bottlenecks, predictable performance

### Configuration Example

```
node "node1" {
  fastname "prodserver1"
  pools "node1" "processing"
  resource disk "/data1/datastage" {pools ""}
  resource disk "/data2/datastage" {pools ""}
  resource scratchdisk "/scratch1/datastage" {pools ""}
  resource scratchdisk "/scratch2/datastage" {pools ""}
  resource scratchdisk "/scratch3/datastage" {pools ""}
}

Physical: /data1-2 → SSD RAID 10 (1 TB each), /scratch1-3 → SSD RAID 0 (500 GB each)
Result: 2 TB resource, 1.5 TB scratch, parallel I/O across 5 disks
```

---

## Resource Pool Management

Resource pools are named groups of nodes for logical resource allocation and workload management. Use them to control where jobs run, isolate workloads, and optimize resource usage.

### Configuration

```
node "etl_node1" {
  fastname "etlserver1"
  pools "etl_pool" "general"
  resource disk "/data" {pools ""}
  resource scratchdisk "/scratch" {pools ""}
}

node "db_node1" {
  fastname "dbserver1"
  pools "db_pool" "database"
  resource disk "/data" {pools ""}
  resource scratchdisk "/scratch" {pools ""}
}

Pools: etl_pool (ETL nodes), db_pool (database nodes), general (all nodes)
```

### Using Resource Pools

**Job-Level Pool Selection:**
```
Job Configuration:
- Execution Mode: Parallel
- Resource Pool: etl_pool

Result:
✓ Job runs only on ETL nodes
✓ Does not use database nodes
✓ Isolated from database workload
```

**Stage-Level Pool Selection:**
```
Database Connector Stage:
- Resource Pool: db_pool

Result:
✓ Database operations run on database nodes
✓ Close to database
✓ Reduced network traffic
✓ Optimal database access
```

---

## Resource Pool Strategies

### Strategy 1: Workload Isolation

```
Pools:
- batch_pool: Batch processing
- realtime_pool: Real-time processing
- reporting_pool: Reporting jobs

Benefits:
✓ No interference between workloads
✓ Guaranteed resources for each type
✓ Predictable performance
✓ Better SLA compliance
```

### Strategy 2: Priority-Based Allocation

```
Pools:
- high_priority: Critical jobs
- medium_priority: Standard jobs
- low_priority: Background jobs

Resource Allocation:
- high_priority: 8 nodes, 64 partitions
- medium_priority: 4 nodes, 32 partitions
- low_priority: 2 nodes, 16 partitions

Benefits:
✓ Critical jobs get best resources
✓ Background jobs don't interfere
✓ Flexible resource management
```

### Strategy 3: Database Co-location

```
Scenario: Database and DataStage on same servers

Pools:
- db_local: Nodes with database
- etl_only: Nodes without database

Usage:
Database Stages → db_local
- Minimize network traffic
- Direct database access
- Optimal performance

Transform Stages → etl_only
- Don't compete with database
- Dedicated ETL resources
- No database interference

Benefits:
✓ Reduced network traffic
✓ Better database performance
✓ Isolated workloads
✓ Optimal resource usage
```

### Strategy 4: Data Locality

```
Scenario: Data distributed across nodes

Pools:
- data_zone1: Nodes with zone 1 data
- data_zone2: Nodes with zone 2 data
- data_zone3: Nodes with zone 3 data

Usage:
Jobs processing zone 1 data → data_zone1
Jobs processing zone 2 data → data_zone2
Jobs processing zone 3 data → data_zone3

Benefits:
✓ Data locality
✓ Reduced data movement
✓ Better performance
✓ Network efficiency
```

---

## Summary

**Key Takeaways:**

### Disk Optimization:
1. **Use multiple local disks** for scratch and resource storage
2. **Prefer SSDs** for best performance
3. **Separate scratch and resource disks** to avoid contention
4. **Use RAID 0 for scratch**, RAID 10 for resource disks
5. **Ensure adequate space** with safety margins

### Resource Pool Management:
1. **Define pools** for workload isolation
2. **Use job-level pools** for overall execution control
3. **Use stage-level pools** for database optimization
4. **Implement priority-based** allocation for SLA compliance
5. **Leverage data locality** to reduce network traffic

**Performance Impact:**
- Proper disk configuration: 2-5x performance improvement
- Resource pool optimization: 30-50% better resource utilization
- Combined optimization: Significant throughput gains

**Success Factors:**
- Local, fast disks (SSDs preferred)
- Multiple disks for parallel I/O
- Proper RAID configuration
- Strategic resource pool design
- Workload isolation
- Regular monitoring and tuning