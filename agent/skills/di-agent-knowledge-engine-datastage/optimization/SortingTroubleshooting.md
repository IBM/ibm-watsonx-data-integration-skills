# DataStage Sorting Troubleshooting

## Problem: Sort Running Slowly
**Symptoms:** Sort taking excessive time  
**Causes:**
- Too many sort keys
- Insufficient memory (disk spill)
- Stable sort enabled unnecessarily
- Multiple sorts in flow

**Solutions:**
- Reduce sort keys to minimum necessary
- Increase memory allocation
- Disable stable sort if not needed
- Minimize sorts in job flow

---

## Problem: Out of Memory Errors
**Symptoms:** Job fails with memory errors during sort  
**Causes:**
- Sort memory too high
- Insufficient system memory
- Large data volume

**Solutions:**
- Reduce memory restriction
- Enable disk spill
- Increase system memory
- Partition data more finely

---

## Problem: Incorrect Sort Order
**Symptoms:** Output not sorted as expected  
**Causes:**
- Wrong sort keys
- Incorrect sort order (Asc/Desc)
- Case sensitivity issues
- Missing Sort Merge collector

**Solutions:**
- Verify sort keys match requirements
- Check sort order configuration
- Review case sensitivity settings
- Add Sort Merge collector for sequential output

---

## Problem: Multiple Unnecessary Sorts
**Symptoms:** Job has many sort operations  
**Causes:**
- Auto-inserted sorts
- Redundant explicit sorts
- Not preserving sort order

**Solutions:**
- Use APT_SORT_INSERTION_CHECK_ONLY to identify
- Add explicit sorts in optimal locations
- Use Same partitioning to preserve order
- Combine sort requirements