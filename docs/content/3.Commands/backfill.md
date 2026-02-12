---
title: Backfill
description: Backfills historical jobs into the unprocessed jobs list
navigation:
  icon: i-lucide-file-clock
---

## Usage

```bash [Terminal]
guilt backfill
```

## Description

The GUILT `backfill` command is used to backfill historical jobs into the unprocessed jobs list.
This is particularly useful when initially setting up GUILT on an HPC system that has been in use for some time, as it allows users to process and analyze jobs that were executed prior to GUILT's installation.

## How it works

GUILT collects previous jobs ran on the HPC system by querying the SLURM accounting database.

It does this by parsing the following SLURM command's output:

```bash [Terminal]
sacct --user $USER --starttime 1970-01-01 --json
```

Once this is parsed, GUILT identifies jobs that have not yet been processed and adds them to the unprocessed jobs list for further analysis.

Unlike jobs that are submitted using `guilt batch` where a CPU Profile name is specified in the script directives, backfilled jobs are assigned `"None"` for their `cpu_profile_resolution_data` field.
Later, when these backfilled jobs are processed, GUILT will pass data from the `sacct` command to your [Profile Resolution Policy](/how-it-works/profile-resolution) to determine which CPU Profile to use for each job.
