# Sort Merge Collector for Sequential Ordered Output

## When to Use

Use Sort Merge Collector when you need a **single output file with all records in sorted order**.

## The Problem

Parallel Sort alone creates multiple sorted partitions, not a single sorted sequence. A Sort Merge Collector is required to merge sorted partitions.

## The Solution: Sort + Sort Merge Collector

**Two-Step Process:**
1. **Parallel Sort** - Sorts data within each partition (fast, parallel)
2. **Sort Merge Collector** - Merges sorted partitions into single sorted sequence

## Implementation

### Method 1: Using Sort Stage

```
Job Flow:
Source → Sort Stage → Sequential File
         (parallel)   (Sort Merge collector)

Sort Stage Configuration:
- Sort Keys: customer_id
- Partitioning: Auto or Hash

Sequential File Configuration:
- Collection Method: Sort Merge ✅
- Merge Keys: customer_id (MUST match sort keys)
```

### Method 2: Using Link Sort

```
Job Flow:
Source → Link (with sort) → Sequential File
                            (Sort Merge collector)

Link Configuration:
- Sort Keys: customer_id

Sequential File Configuration:
- Collection Method: Sort Merge ✅
- Merge Keys: customer_id
```

## Complete Example

**Requirement:** Export all customers sorted by customer_id to single file

**Configuration:**

1. Sort Stage:
   - Input: Customer data (partitioned)
   - Sort Keys: customer_id
   - Sort Order: Ascending
   - Output: Sorted partitions

2. Sequential File Stage:
   - Input: Sorted partitions
   - Collection Method: Sort Merge ✅
   - Merge Keys: customer_id
   - Output: Single sorted file

**Result:**
- ✅ All records in single file
- ✅ Sorted by customer_id
- ✅ Efficient parallel processing

## Performance Characteristics

```
Parallel Sort:
- Time: O(n log n) per partition
- Parallelized across nodes
- Fast

Sort Merge Collector:
- Time: O(n) for merge
- Sequential operation
- Relatively fast

Total: Much faster than sequential sort of all data
```

## Alternative (NOT Recommended)

```
Sequential Sort (entire data set):
❌ Slow (no parallelism)
❌ High memory usage
❌ Single bottleneck

Use parallel sort + merge instead! ✅
```

## Critical Configuration

**MUST match sort keys:** The merge keys in the Sequential File stage MUST exactly match the sort keys used in the Sort Stage or Link Sort, including:
- Same columns
- Same order
- Same sort direction (Asc/Desc)