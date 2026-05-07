# Data Set Usage for Performance

## Overview
Data Sets are DataStage's native parallel file format, optimized for maximum performance in parallel processing environments. This guide explains when and how to use Data Sets effectively.

---

## The Data Set Advantage

**Core Principle:**
> When writing intermediate results that will only be shared between parallel jobs, always write to persistent data sets (using Data Set stages).

### What are Data Sets?

```
Definition:
- Native parallel file format
- Preserves partitioning
- Maintains sort order
- No format conversion
- Optimized for parallel I/O

Structure:
- Multiple files (one per partition)
- Binary format
- Metadata included
- Platform-specific
```

### Why Use Data Sets?

**1. Maximum Performance:**

Data Sets are specifically designed for parallel processing with minimal overhead and no format conversions, making them the fastest way to move data between parallel jobs. In contrast, sequential files require format conversion and introduce significant overhead, and can become a performance bottleneck due to sequential I/O operations.

**2. Preserved Partitioning:**
Data Sets preserve partitioning for downstream stages, avoiding repartitioning and redistribution overhead, whereas Sequential Files lose partitioning and require costly data reshuffling.

**3. Preserved Sort Order:**
Data Sets preserve sort order for downstream processing, eliminating re-sorting and saving time, whereas Sequential Files lose sort order and require additional sorting overhead.

--- 

## Data Set Best Practices

### Guideline 1: Ensure Proper Partitioning

> You should ensure that the data is partitioned, and that the partitions, and sort order, are retained at every stage.

**Implementation:**
```
Job Flow:
Source → Transform → Data Set → Process → Data Set → Target

At Each Data Set:
1. Verify partitioning method
2. Confirm partition count
3. Check sort order
4. Validate data distribution
```

**Example: Optimal Data Flow**
```
Job 1: Extract and Prepare
Source → Hash Partition (customer_id) → 
Sort (customer_id, date) → 
Data Set (partitioned, sorted)

Job 2: Process
Data Set (partitioned, sorted) → 
Same Partition (preserves) → 
Aggregator (uses sort) → 
Data Set (partitioned)

Job 3: Load
Data Set (partitioned) → 
Same Partition (preserves) → 
Target
```

### Guideline 2: Avoid Format Conversion

> Avoid format conversion or serial I/O.

**What to Avoid:**

**Format Conversion:**
```
❌ Data Set → Sequential File → Data Set
   (Binary → Text → Binary conversion overhead)

✅ Data Set → Data Set
   (No conversion, direct binary)

Format conversion is 50-80% slower, while direct binary offers optimal speed
```

**Serial I/O:**
```
❌ Data Set → Sequential File (single file)
   (Parallel → Serial bottleneck)

✅ Data Set → Data Set (multiple files)
   (Parallel → Parallel, no bottleneck)

Performance Impact:
Serial I/O: Limited by single disk/file
Parallel I/O: Scales with partition count
```

---

## Complete Example

**Scenario: Multi-Job Processing**
```
Requirement:
- Extract 100 million records
- Transform data
- Aggregate by customer
- Load to target

Poor Design (Sequential Files):
Job 1: Extract → Transform → Sequential File
Job 2: Sequential File → Aggregate → Sequential File
Job 3: Sequential File → Load

Issues: Format conversion at each stage, serial I/O, no parallelism, lost partitioning and sort order, slow performance 

Good Design (Data Sets):
Job 1: Extract → Transform → Data Set (partitioned, sorted)
Job 2: Data Set → Aggregate → Data Set (partitioned)
Job 3: Data Set → Load

Benefits: No format conversion, parallel I/O, preserved partitioning, preserved sort order, optimal performance

Performance Comparison:
Sequential Files: 120 minutes
Data Sets: 25 minutes
```
---

## Data Set Limitations

### Not for Long-Term Backup

**Important Limitation:**
> Because data sets are platform and configuration specific, they should not be used for long-term backup and recovery of source data.


### Proper Backup Strategy

```
Short-Term (Restart Points):
✓ Use Data Sets
✓ Within same job run
✓ Same configuration
✓ Temporary storage

Long-Term (Backup/Archive):
✓ Use Sequential Files
✓ Use Database tables
✓ Use standard formats (CSV, Parquet, etc.)
✓ Platform-independent
✓ Configuration-independent

Example:
Daily Processing:
- Use Data Sets for restart points
- Delete after successful completion

Monthly Archive:
- Export to Sequential Files
- Store in archive location
- Platform-independent format
- Long-term retention
```

---

## Summary

**Key Takeaways:**

1. **Use Data Sets for intermediate results** between parallel jobs
2. **Preserve partitioning and sort order** throughout the flow
3. **Avoid format conversion** and serial I/O
4. **Use for restart points** but not long-term backup
5. **Performance gains** can be 4-5x compared to Sequential Files

**When to Use Data Sets:**
- ✅ Intermediate results between jobs
- ✅ Restart points within processing
- ✅ Temporary storage during job execution
- ✅ Performance-critical data flows

**When NOT to Use Data Sets:**
- ❌ Long-term backup/archive
- ❌ Cross-platform data exchange
- ❌ External system integration
- ❌ Data that needs to survive configuration changes