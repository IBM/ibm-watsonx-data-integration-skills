# Sort Stage Advanced Configuration

This document provides detailed configuration options for the Sort Stage. Reference this when you need advanced features beyond basic Link Sort.

## Memory Control

### Restrict Memory Usage
Restrict sort memory to control resource usage and prevent instability.

**Configuration:**
```
Sort Stage Properties:
- Options Tab
- Restrict Memory Usage (MB): [value]

Example: 512 (limits sort to 512 MB per partition)
```

**Alternative: Environment Variable**
```
APT_TSORT_STRESS_BLOCKSIZE=<MB>
```

**Memory Sizing Guidelines:**
```
Data Volume per Partition → Sort Memory:
- < 100 MB → 128 MB
- 100 MB - 500 MB → 256 MB
- 500 MB - 2 GB → 512 MB
- > 2 GB → 1024 MB or more

Formula: Sort Memory = Data Volume × 1.5 to 2.0
```

Memory should be restricted when system memory is limited or multiple jobs are running concurrently
Memory can be increased when sort performance is critical, disk spill needs to be minimized, and sufficient RAM is available
---

## Sort Key Mode: "Don't Sort (Previously Sorted)"

**Use Case:**
Data is already sorted on primary key, need to sort on secondary key within groups

**Configuration:**
- Sort Key Mode: Don't Sort (Previously Sorted)
- Primary Keys: customer_id (already sorted, don't re-sort)
- Secondary Keys: date (sort within customer groups)

**Benefits:**
- Faster than full re-sort
- Preserves primary sort order
- Efficient for hierarchical sorting

---

## Create Cluster Key Change Column

**Purpose:**
Adds column indicating when sort key values change (group boundaries)

**Use Cases:**
- Identifying first record in a group
- Triggering actions on key changes
- Group boundary detection
- Custom aggregation logic

**Configuration:**
```
- Options → Create Cluster Key Change Column: True
- Column Name: <flag_column>
```

---

## Output Statistics

**Purpose:**
Provides sorting performance statistics for analysis that can be enables for tuning or troubleshooting.

**Statistics Provided:**
- Number of records sorted
- Memory used
- Disk spill information
- Sort time

---

## ALWAYS Specify DataStage Sort Utility

**Critical Configuration:**
**Always select "DataStage" as Sort Utility for Sort stages**

**Why This Matters:**
```
DataStage Sort:
✅ Optimized for parallel processing
✅ Integrated with DataStage framework
✅ Handles partitioned data efficiently
✅ Supports all DataStage data types

External Sort:
❌ Not optimized for DataStage
❌ May not handle partitions correctly
❌ Limited data type support
❌ Performance issues