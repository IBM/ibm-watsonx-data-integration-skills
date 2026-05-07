# DataStage Partitioning Guide

## Purpose
This guide provides explicit decision criteria for selecting DataStage partitioning methods. Use this to determine the optimal partitioning strategy based on data characteristics and stage requirements.

---

---

## Critical Rules

1. **Hash/Modulus/Range for grouping stages** - Required for correct results
2. **Same preserves upstream** - Zero overhead but inherits issues
3. **Round Robin breaks grouping** - Only use when no grouping needed
4. **Modulus only for single integer keys** - Don't use for other types
5. **Range requires maintenance** - Only use for severe, stable skew
6. **Auto is safe but may not be optimal** - Good starting point

## Partitioning Methods: When to Use Each

### 1. AUTO Partitioning
**Use When:**
- Designing a new job 
- Data characteristics are unknown
- Quick development needed
- Job requirements are straightforward

**Characteristics:**
- Engine selects method automatically
- Guarantees correct results
- May not be performance-optimal
- No configuration required
- Best starting point 

---

### 2. HASH Partitioning

**Use When:**
- Stage requires grouping of related records
- Multiple key columns needed
- Normal (non-skewed) data distribution
- Key has high cardinality (many unique values)
- Required for Aggregator, Join, Merge, Remove Duplicates, Sort, Change Capture/Apply

**Key Selection Rules:**
- High cardinality 
- Minimum unique values: >= degree of parallelism
- Recommended: 10x node count, Optimal: 100x+ node count

---

### 3. MODULUS Partitioning
**Use When:**
- Grouping on SINGLE INTEGER key only
- Key is sequential or evenly distributed
- Performance optimization needed

**Advantages Over Hash:**
- Faster and lower CPU overhead
- Guaranteed even distribution for sequential keys

**Do NOT Use When:**
- Key is not integer type
- Multiple key columns needed
- Sparse or irregular key ranges
---

### 4. RANGE Partitioning

**Use When:**
- Data is HIGHLY skewed (>80% in few values)
- Key value distribution is STABLE over time
- A range map can be created and reused
- Re-partitioning cost is high

**Trade-Off:**
- Best balance for extreme skew, but highest operational complexity
- Requires ongoing maintenance
- Use ONLY when skew is severe and stable


### 5. ROUND ROBIN Partitioning
**Use When:**
- NO grouping required
- Need perfectly even distribution
- Input is skewed or sequential

**Perfect For:**
- Sequential file input (single partition → parallel)
- Skewed upstream data that needs rebalancing
- Stages with no grouping requirements (Filter, Transformer without grouping)

Never use when grouping is required.


### 6. SAME Partitioning
**Use When:**
- Upstream partitioning is appropriate
- No grouping requirement changes
- Want to avoid re-partitioning cost
- Preserving sort order from upstream

**Benefits:**
- Zero overhead (no data movement)
- Preserves partition and sort order
- Optimal for multi-stage flows

**Caution:**
- Inherits upstream degree of parallelism
- Inherits upstream data skew
- Only use if upstream partitioning is correct

---

### 7. ENTIRE Partitioning
**Use When:**
- All records must go to single partition
- Very small data volume
- Stage requires all data together

This approach Eliminates parallelism completely and creates bottleneck

---

### 8. RANDOM Partitioning
**Use When:**
- Rarely used (prefer Round Robin)
- Non-deterministic distribution acceptable
- Even distribution needed

**Difference from Round Robin:**
- Random: Non-deterministic, unpredictable
- Round Robin: Deterministic, predictable

**Recommendation:** Use Round Robin instead

---

## Decision Tree

```
START: Need to partition data?
│
├─ Does stage require GROUPING?
│  │
│  ├─ YES → Use Hash/Modulus/Range
│  │  │
│  │  ├─ Is key a SINGLE INTEGER?
│  │  │  └─ YES → Use MODULUS
│  │  │
│  │  ├─ Is data HIGHLY SKEWED (>80% in few values)?
│  │  │  ├─ YES + Distribution STABLE → Use RANGE
│  │  │  └─ YES + Distribution CHANGES → Use HASH (accept skew)
│  │  │
│  │  └─ Normal distribution → Use HASH
│  │
│  └─ NO → Need even distribution?
│     │
│     ├─ YES (input skewed/sequential) → Use ROUND ROBIN
│     │
│     └─ NO (upstream good) → Use SAME
│
└─ Starting new job? → Use AUTO, then optimize
```

---

## Stage Requirements Quick Reference

| Stage | Requires Grouping? | Recommended Method | Key Columns |
|-------|-------------------|-------------------|-------------|
| Aggregator | ✅ YES | Hash/Modulus | Grouping keys |
| Join | ✅ YES | Hash | Join keys (all inputs) |
| Merge | ✅ YES | Hash | Merge keys |
| Remove Duplicates | ✅ YES | Hash | Key columns |
| Sort | ✅ YES | Hash | Sort keys |
| Change Capture | ✅ YES | Hash | Key columns |
| Change Apply | ✅ YES | Hash | Key columns |
| Lookup | ❌ NO | Any | N/A |
| Transformer | ⚠️ DEPENDS | Hash if grouping | Group keys if needed |
| Filter | ❌ NO | Same/Round Robin | N/A |
| Funnel | ❌ NO | Any | N/A |
| Copy | ❌ NO | Same | N/A |

---

##  Key Design Patterns
- Sequential File Input → Round Robin to enable parallelism
- Repeated processing on same key → Hash once, then Same
- Skewed data → Accept skew (Hash) or manage explicitly (Range)
- Multiple grouping requirements → Expect repartitioning or split jobs


## Core Principles

1. **Start with Auto** - Always begin with Auto partitioning
2. **Identify Grouping** - Determine if stage requires grouped records
3. **Choose Keys Carefully** - High cardinality, even distribution
4. **Minimize Re-partitioning** - Use Same when possible
5. **Balance Distribution** - Use Round Robin for skewed inputs
6. **Optimize for Integers** - Use Modulus for single integer keys
7. **Handle Skew** - Use Range only if skew is severe and stable

---

## Performance Impact
- Parallel job runtime equals the slowest partition
- Skewed partitioning can make jobs 3–4× slower

## Optimization Checklist

- [ ] Identified stage grouping requirements
- [ ] Analyzed data distribution and cardinality
- [ ] Selected appropriate partitioning method
- [ ] Verified key column selection
- [ ] Minimized re-partitioning operations
- [ ] Used Same to preserve good partitioning
- [ ] Tested with representative data volumes
- [ ] Monitored for partition skew
- [ ] Documented partitioning decisions