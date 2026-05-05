# Restart Points and Recovery

## Overview
Using Data Sets as restart points enables quick recovery from job failures by avoiding the need to reprocess entire workflows. This guide explains how to implement effective restart strategies.

---

## Using Data Sets for Restart Points

**Core Principle:**
> Data Set stages should be used to create restart points in the event that a job or sequence needs to be rerun.

### Why Restart Points Matter

```
Scenario: Long-Running Job Fails
Without Restart Points:
- Entire job must rerun
- All processing repeated
- Wasted time and resources
- Extended recovery time

With Restart Points:
- Resume from last checkpoint
- Only reprocess failed portion
- Minimal wasted effort
- Quick recovery
```

---

## Restart Point Strategy

### Where to Place Restart Points

```
1. After Expensive Operations:
   - Complex transformations
   - Large aggregations
   - Extensive joins
   - Time-consuming processes

2. At Logical Boundaries:
   - End of extraction
   - After data cleansing
   - Before loading
   - Between major phases

3. For Long-Running Jobs:
   - Every 30-60 minutes of processing
   - After significant milestones
   - Before risky operations
```

---

## Best Practices

### 1. Strategic Placement

**Place restart points:**
- After expensive operations that you don't want to repeat
- At natural boundaries in your processing logic
- Before operations with higher failure risk
- At intervals in long-running jobs (30-60 minutes)

### 2. Cleanup Strategy

**Manage restart point Data Sets:**
```
During Processing:
- Keep Data Sets until job sequence completes
- Use for recovery if needed

After Successful Completion:
- Delete temporary restart point Data Sets to free up disk space
- Maintain only necessary checkpoints

After Failure:
- Keep Data Sets for restart
- Investigate failure
- Rerun from appropriate checkpoint
- Clean up after successful rerun
```

### 3. Naming Convention

**Use clear, descriptive names:**
```
Examples:
- DS_Extract_Complete
- DS_Cleansed_Data
- DS_Aggregated_Results
- DS_PreLoad_Checkpoint

```

### 4. Documentation

**Document restart strategy:**
- List all restart points
- Describe what each checkpoint contains
- Specify recovery procedures
- Note dependencies between jobs

---

## Recovery Procedures

### Standard Recovery Process

```
1. Identify Failure Point: Review job logs to determine the last successful checkpoint

2. Verify Data Sets: Confirm availability and integrity of restart point Data Sets

3. Restart from Checkpoint: Start from the appropriate dataset, running subsequent jobs

4. Monitor Execution: Watch for errors, verify data quality, confirm completion

5. Clean Up: Remove temporary Data Sets, archive logs, document any issues

```

### Example Recovery Scenario

```
Scenario: 4-Job Sequence Fails at Job 3

Original Sequence:
Job 1: Extract → DS1 ✓ (Completed)
Job 2: Cleanse → DS2 ✓ (Completed)
Job 3: Aggregate → DS3 ✗ (Failed)
Job 4: Load (Not started)

Recovery Steps:
1. Verify DS2 exists and is valid
2. Fix issue that caused Job 3 failure
3. Restart sequence from Job 3:
   - Job 3: DS2 → Aggregate → DS3
   - Job 4: DS3 → Load → Target
4. Monitor completion
5. Clean up DS1, DS2, DS3 after success

Time Saved:
- Without restart points: Rerun all 4 jobs (120 min)
- With restart points: Rerun jobs 3-4 only (40 min)
- Savings: 80 minutes (67% faster recovery)
```

---

## Limitations and Considerations

### Data Set Limitations

**Important:** Data Sets are for short-term restart points, not long-term backup.

**Limitations:**
- Platform-specific (not portable)
- Configuration-specific (node count, paths)
- Version-specific (may not survive upgrades)

**For long-term backup, use:**
- Sequential Files
- Database tables
- Standard formats (CSV, Parquet)

**See:** [Data Set Performance Guide](DataSetPerformance.md) for detailed limitations

### Disk Space Management

**Consider disk space:**
- Check disk space before creating Data Sets

---

## Summary

**Key Takeaways:**

1. **Use Data Sets for restart points** to enable quick recovery
2. **Place strategically** after expensive operations and at logical boundaries
3. **Clean up after success** to free disk space
4. **Document recovery procedures** for operational teams
5. **Not for long-term backup** - use platform-independent formats instead

**Benefits:**
- Faster recovery from failures
- Reduced reprocessing time
- Lower resource usage
- Improved operational efficiency
- Better risk management

**Recovery Time Savings:**
- Without restart points: 100% reprocessing
- With restart points: 20-40% reprocessing (typical)
- Time savings: 60-80% faster recovery