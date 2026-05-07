# Memory Management Best Practices

## Overview
DataStage NextGen jobs running in CP4D or SaaS run inside containers with memory limits so it is important to understand how memory is used during runtime to avoid container restarts or OOM kills.

## Connectors
  - Most connectors are Java based and use JVM heap memory which defaults to 256MB which means they use much more memory than builtin stages.
  - JVM heap is configurable through the stage options or for the entire job with CC_JVM_OPTIONS environment variable.
  - JVM heap may need to be increased for connectors that require more memory to process a particular data set.
  - Be aware that memory usage during job run for each connector stage in the job will be multiplied by the number of partitions if running in parallel on partitioned tables.
  - Many connectors use in memory buffering with a default prefetch size of 2000 records. If the schema being read includes large string or binary columns like CLOBs, BLOBs, or VARCHAR(MAX) columns, this can lead to OOM issues. Reduce the prefetch size or disable record buffering if necessary.

## Engine Transport Blocks
  - For every stage link in memory buffers are created for passing data between stages running in the same container.
  - The default size of the in memory transport buffers is 128KB.
  - The default number of in memory buffers created for each stage link is 2
  - The size of all transport buffers in the can be confgured by setting APT_DEFAULT_TRANSPORT_BLOCK_SIZE environment variable in bytes.
  - Note that as the number of stages increases and the partition count increases the total memory required for the in memory buffers can become significant.
  - Repartitioning within a flow greatly increases the number of transport buffers as it requires every upstream stage to have a connection to every downstream stage.

## Sorting
  - Every partition of each sort stage allocates an in memory buffer to sort deta
  - The default size of the in memory sort buffer is 20MB
  - The size of the in memory sort buffer is configurable on the specific sort stage or job wide by setting APT_DEFAULT_TRANSPORT_BLOCK_SIZE in bytes

## Joins
  - Joins by default do not allocate a fixed amount of memory, but dynamically allocate memory as records are read.
  - The number of records with duplicate key values in the reference link determines the amount of memory allocated.
  - When joining tables it is almost always best to use the smaller table as the reference link to reduce memory usage.

## Lookups
  - Lookups use the system mmap function to map the lookup table data into memory.
  - The amount of memory and disk used by the lookup table is determined by the size of the lookup table data.
  - To avoid high memory usage prefer join, merge or pushing the lookup into a database.

## Merges
  - The merge stage has similar dynamic memory allocation as joins.

## Aggregations
  - Be aware that large aggregations can require dynamic allocation of a large amount of memory.

## Buffers
  - Buffer operators are inserted automatically into DataStage jobs with fork join patterns to avoid data deadlock.
  - Buffer operators allocate an in memory buffer to store records as they are processed before writing to disk if the buffer fills up.
  - The default size of the in memory buffer is 3MB.
  - The size of the in memory buffer can be configured with the specific stage setting or job wide by setting APT_BUFFER_MAXIMUM_MEMORY in bytes.
