# Concurrent Job Execution

## Overview
Running multiple DataStage jobs concurrently can significantly reduce overall processing time when system resources are available. This guide explains how to plan, implement, and manage concurrent job execution effectively.

---

## Optimizing with Concurrent Jobs

**Core Principle:**
> Depending on available system resources, it might be possible to optimize overall processing time at run time by allowing smaller jobs to run concurrently, enabling significant speedups. Concurrency works when there is sufficient CPU capacity, memory, and I/O bandwidth to handle multiple jobs simultaneously. The jobs also need to be independent and not share critical resources.
---


### Resource Planning

1. **Measure individual job requirements** (CPU, memory, I/O)
2. **Calculate total available resources**
3. **Determine concurrent capacity** (don't use 100%)
4. **Reserve capacity for overhead** and unexpected loads
5. **Plan for failure recovery** 

**Example:**
```
Job Requirements:
Job A: 8 cores, 32 GB, 500 MB/s I/O
Job B: 8 cores, 32 GB, 500 MB/s I/O
Job C: 8 cores, 32 GB, 500 MB/s I/O

Available Resources:
- CPU: 32 cores
- Memory: 128 GB
- Disk I/O: 2 GB/s
- Network: 10 Gb/s

Concurrent Capacity:
Can run 3 jobs concurrently:
- CPU: 24/32 cores (75%)
- Memory: 96/128 GB (75%)
- I/O: 1.5/2 GB/s (75%)

Result: ✓ Concurrency feasible
```

### Dependency Patterns and Management: 

**1. Independent Jobs (No Dependencies):**
```
Job A ─┐
Job B ─┼─→ All can run concurrently
Job C ─┘

Best for: Maximum concurrency
```

**2. Fan-In Pattern:**
```
Job A ─┐
Job B ─┼─→ Job D
Job C ─┘

Phase 1: A, B, C concurrent
Phase 2: D after all complete
```

**3. Fan-Out Pattern:**
```
       ┌─→ Job B
Job A ─┼─→ Job C
       └─→ Job D

Phase 1: A runs first
Phase 2: B, C, D concurrent
```

**4. Mixed Dependencies:**
```
Job A ─→ Job C ─┐
Job B ─→ Job D ─┼─→ Job F
       Job E ───┘

Requires careful sequencing
```

---

## Handling Late Arrivals and Failures

> Care must be taken to plan for scenarios when source files arrive later than expected, or need to be reprocessed in the event of a failure.

**Scenario 1: File Dependency**
```
Expected:
File A arrives: 8:00 AM
File B arrives: 8:00 AM
File C arrives: 8:00 AM
All jobs start: 8:00 AM

Reality:
File A arrives: 8:00 AM
File B arrives: 8:00 AM
File C arrives: 8:30 AM (LATE)

Handling:
Option 1: Wait for all files
- Jobs A, B wait for C
- Start all at 8:30 AM
- Concurrent execution

Option 2: Start available jobs
- Jobs A, B start at 8:00 AM
- Job C starts at 8:30 AM
- Partial concurrency

```

**Scenario 2: Job Failure During Concurrent Execution**
```
Concurrent Execution:
Job A: Success ✓
Job B: Failed ✗
Job C: Success ✓

Reprocessing:
- Rerun Job B only
- Jobs A, C already complete
- Use restart points if available

Considerations:
- Does Job B failure affect downstream?
- Can Job B rerun independently?
- Are resources available for rerun?
- What is the recovery time?
```

---

## Best Practices for Concurrency

### 1. Monitor File Arrivals
   - Check file availability before starting
   - Wait for all dependencies
   - Alert on delays
   - Have fallback plans
   - Implement timeout logic


### 2. Implement Error Handling
   - Graceful failure handling
   - Independent job recovery
   - Restart point usage, see [Restart and Recovery Guide](RestartAndRecovery.md) for details 
   - Notification mechanisms
   - Automated retry logic


### 3. Resource Reservation
   - Reserve capacity for reruns (don't use 100%)
   - Allow for unexpected loads
   - Plan for peak times
   - Monitor resource usage and adjust concurrency dynamically

### 4. Dependency Tracking
   - Document all dependencies
   - Use job sequencers
   - Implement wait conditions
   - Validate prerequisites

### 5. Testing
   - Test concurrent execution
   - Simulate failures and late arrivals
   - Validate recovery procedures
   - Measure actual resource usage
---

## Implementation Strategies

### Strategy 1: Fixed Concurrency
-  Run fixed number of jobs concurrently. This is best for stable workloads, with known resource requirements and simple dependencies.

### Strategy 2: Dynamic Concurrency
- Adjust concurrency based on resources, works well for variable workloads, shared environments, and unpredictable arrivals. 

### Strategy 3: Priority-Based
- Prioritize critical jobs. This approach is best when we have specific business priorities or SLA requirements that lead to mixed workloads.

---

## Monitoring and Optimization

### Key Metrics to Monitor

1. Resource Utilization: CPU usage, memory consumption, I/O throughput, network bandwidth

2. Execution Times: job completion times, average processing time, wait times, queue depths

3. Success Rates: job completion rates, failure frequencies, recovery times, SLA compliance

4. Concurrency Levels: concurrent jobs, resource contention, bottlenecks

### Optimization Techniques

1. Adjust Concurrency:
   - Increase if resources underutilized
   - Decrease if contention occurs
   - Balance throughput vs. resource usage

2. Reorder Jobs:
   - Run longest jobs first
   - Group similar resource profiles
   - Minimize wait times

3. Resource Allocation:
   - Tune job configurations
   - Optimize memory settings
   - Balance I/O distribution

4. Dependency Optimization:
   - Reduce unnecessary dependencies
   - Parallelize where possible
   - Use restart points strategically
---

## Summary

**Key Takeaways:**

1. **Concurrency can significantly reduce processing time** (2-3x faster typical)
2. **Plan resource capacity carefully** - don't use 100%
3. **Handle dependencies properly** using job sequencers
4. **Prepare for late arrivals and failures** with robust error handling
5. **Monitor and optimize continuously** based on actual performance