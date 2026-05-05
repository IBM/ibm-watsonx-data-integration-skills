# DataStage Sorting Configuration Guide

## Purpose
This guide provides explicit instructions for sorting data in DataStage parallel jobs, focusing on performance optimization and correct configuration. Use this to minimize sorting overhead and ensure efficient data processing.

---

## 7 Step Sorting Methodology

1. Start with Link Sort (simplest)
2. Specify only necessary key columns
3. Avoid Stable Sort unless needed (high performance cost)
4. Use Sort Stage for advanced options where link sort is insufficient
5. Monitor automatic sort insertion 
6. Minimize sorts in flow (sort once, preserve order)
7. Use Sort Merge collector to generate sequential ordered results

## Best Practices

**Do**: Start with Link Sort, minimize sort keys, use Sort Stage for advanced options, monitor auto-inserts, use Sort Merge for sequential output, always use DataStage sort utility, control memory usage, document requirements

**Don't**: Over-sort, use Stable Sort by default, ignore auto-inserts, use external sort utilities, sort on too many keys, forget memory limits, re-sort unnecessarily, use sequential sort

---

## Step 1 : Link Sort vs. Sort Stage

**Use Link Sort**: Simple requirements, standard options (ascending/descending), no memory constraints, no advanced features are required - use this for simple sorting needs

**Use Sort Stage**: Need to control memory usage, require "Don't Sort (Previously Sorted)" mode, want key change columns, need sorting statistics, have complex requirements,or when performance tuning is critical - use this for advanced sorting needs

## Link Sort Example
```
Source → Link (Sort on customer_id) → Aggregator
Link Properties: Sort Keys=customer_id, Sort Order=Ascending
- Case Sensitive: No
- Stable Sort: No
```
---

## Step 2: Specify Only Necessary Key Columns

Only sort on columns required by downstream stage or business logic. Reduces overhead, improves performance (2-3x faster with fewer keys).

**Example**: For aggregating sales by customer and product, sort only on `customer_id, product_id` - not transaction_date, store_id, or sales_amount

---

## Step 3: Avoid Stable Sort Unless Needed

Stable sort preserves original order of records with equal keys and thus maintains relative position of duplicate key values,  but it requires additional processing overhead.

**Use only when**: Business requirement to preserve original order, multiple sorts on different keys, specific ordering requirements for ties

**Default**: Use standard sort for better performance unless stable sort is specifically required.

---

## Step 4: Use Sort Stage for Advanced Options

Use Sort Stage when Link Sort is insufficient and you need: memory control, "Don't Sort (Previously Sorted)" mode, key change columns, output statistics, or advanced configuration.

**Key Features**: Memory control, sort key mode (skip re-sorting), key change columns (group boundaries), statistics, DataStage sort utility (never external sorts)

**See**: [Sort Stage Advanced Configuration](SortStageAdvancedConfig.md)

---

## Step 5: Monitor Automatic Sort Insertion

DataStage automatically adds sorts when downstream stages (Join, Merge, Remove Duplicates, Aggregator) require sorted input. This happens at compile time and may not be visible in job design.

**Monitor with**:
- `APT_DUMP_SCORE=1` - Check for "tsort" operators in score
- `APT_SORT_INSERTION_CHECK_ONLY=1` - Reports where sorts would be inserted without actually inserting them

**Optimization**: Run with check-only mode, identify insertion points, add explicit sorts in optimal locations, verify improvement

---

## Step 6: Minimize Sorts Within Job Flow

Sorting is expensive (CPU, memory, I/O). Multiple sorts compound overhead and create performance bottlenecks.

**Strategy 1 - Sort Once**: Sort once and fan out to multiple stages instead of sorting multiple times on same key. Benefit: 3x faster, 1/3 memory usage

**Strategy 2 - Preserve Order**: Use "Same" partitioning to preserve sort order across stages

### Strategy 3: Combine Sort Requirements

**If multiple stages need different sorts:**
```
Option 1: Separate branches
Source → Sort(key1) → Process1
       → Sort(key2) → Process2

Option 2: Multi-key sort (if compatible)
Source → Sort(key1, key2) → Process1
                          → Process2
```

### Strategy 4: Use Pre-Sorted Data

**If source data is already sorted:**
```
- Document sort order
- Use "Don't Sort (Previously Sorted)" mode
- Avoid unnecessary re-sorting
```

### Sort Audit Checklist
- [ ] Identify all sorts in job (explicit and auto-inserted)
- [ ] Determine if each sort is necessary
- [ ] Look for opportunities to combine sorts
- [ ] Check if sort order can be preserved
- [ ] Verify source data isn't already sorted
- [ ] Document sort requirements

---

## Step 7: Generate Sequential Ordered Results

**When Needed:** Need a single output file with all records in sorted order


**Solution:** Use Sort Merge Collector to merge parallel sorted partitions into single sorted sequence

**For detailed implementation, see:** [Sort Merge Collector Guide](SortMergeCollector.md)

---

## Decision Tree

```
Need to sort data?
│
├─ Simple requirements?
│  └─ Use Link Sort
│
├─ Need memory control?
│  └─ Use Sort Stage with memory options
│
├─ Need key change columns?
│  └─ Use Sort Stage with key change options
│
├─ Data already sorted on primary key?
│  └─ Use Sort Stage with "Don't Sort (Previously Sorted)" mode
│
├─ Need single sorted output file?
│  └─ Use parallel Sort + Sort Merge collector
│
└─ Multiple stages need same sort?
   └─ Sort once, use Same partitioning to preserve
```

---

## Configuration Checklists

### Link Sort Configuration
- [ ] Sort keys specified (minimum necessary)
- [ ] Sort order correct (Asc/Desc)
- [ ] Case sensitivity set appropriately
- [ ] Null handling defined
- [ ] Stable Sort = No (unless required)

### Sort Stage Configuration
- [ ] Sort keys specified (minimum necessary)
- [ ] Sort Utility = DataStage ✅ (ALWAYS)
- [ ] Memory restrictions set (if needed)
- [ ] Sort Key Mode selected (Don't Sort if pre-sorted)
- [ ] Key change columns configured (if needed)
- [ ] Stable sort = False (unless required)
- [ ] Partitioning method chosen (Hash on sort keys)
- [ ] Output statistics enabled (for monitoring)

### Sort Merge Collector Configuration
- [ ] Collection method = Sort Merge
- [ ] Merge keys MATCH sort keys exactly
- [ ] Key order matches
- [ ] Sort order matches (Asc/Desc)

---

## Troubleshooting

**For detailed troubleshooting guidance, see:** [Sort Troubleshooting Guide](SortingTroubleshooting.md)

---

## Summary

**Key Takeaways:**

1. **Start simple** - Use Link Sort for basic needs
2. **Minimize keys** - Only sort on necessary columns
3. **Avoid stable sort** - Unless specifically required (47% slower)
4. **Use Sort Stage** - For memory control and advanced options
5. **Always use DataStage sort utility** - Never external sorts
6. **Monitor auto-inserts** - Hidden sorts impact performance
7. **Sort once, preserve order** - Use Same partitioning
8. **For sequential output** - Use parallel sort + Sort Merge collector

**Performance Impact:**
- Unnecessary sorts can make jobs 2-3x slower
- Proper sort optimization can improve performance by 60%+
- Memory configuration critical for large datasets

**Remember:** Sorting is expensive - minimize, optimize, and preserve sort order whenever possible.