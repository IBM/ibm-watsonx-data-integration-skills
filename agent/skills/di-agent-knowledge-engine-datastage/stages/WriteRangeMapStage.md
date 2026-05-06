# DataStage Write Range Map Stage

## Purpose
Generate range maps for data partitioning.

## When to Use
- Custom partitioning and performance optimization
- When default partitioning doesn't provide optimal distribution

## When NOT to Use
- When default partitioning is sufficient

## Requirements
- **Link Cardinality**: exactly 1 primary input

## Performance
- Range map generation requires sampling or scanning data
- Well-designed range maps significantly improve performance for some types of key data
- Range maps may have to be updated when data distribution changes significantly

## Property Configuration

### key_properties

Required. An array of Dictionaries. where each dictionary must contain a key named 'key' whose value is the name of a column. The dictionary then contains a key 'asc-desc' which has a value from the following list: 'asc', 'desc'

### rangemap

Required. Name of the file that will hold the range map.