---
title: Process
description: Processes all unprocessed jobs
navigation:
  icon: i-lucide-calculator
---

## Usage

```bash [Terminal]
guilt process
```

## Description

The GUILT `process` command calculates the carbon impact of jobs currently listed in the `unprocessed_jobs.json` file.
It moves these jobs to the `processed_jobs.json` file once the calculations are complete.

## How it works

For more information about converting unprocessed jobs to processed jobs, read about [the job lifecycle](../how-it-works/jobs#job-lifecycle).

::steps{level=4}
#### Retrieve Job Metadata

GUILT begins by reading the list of pending jobs from `~/.guilt/unprocessed_jobs.json`.
For each job ID in this list, it queries the local SLURM accounting database using the `sacct` command.
This retrieves execution details including the job's `start_time`, `end_time`, allocated `partition`, and the list of `nodes` it ran on.

#### Resolve CPU Profile

Once the job metadata is retrieved, GUILT determines which CPU profile to use for the calculation:

- **Explicit Profile:** If the job was submitted via `guilt batch` with a `#GUILT --cpu-profile` directive, that specific profile name is used.
- **Dynamic Resolution:** For backfilled jobs or those without an explicit directive, GUILT executes your configured **Profile Resolution Policy**. This is a Rhai script (`profile_resolution_policy.rhai`) that takes the job's `partition` and `nodes` as input and returns the name of the corresponding CPU profile (e.g., "AMD EPYC 7742").

GUILT then looks up the technical specifications (TDP and core count) for this profile in your `~/.guilt/cpu_profiles.json` collection.

#### Fetch Carbon Intensity

Using the job's precise start and end times, GUILT queries the configured carbon intensity API (e.g., `carbonintensity.org.uk`) to retrieve historical data for that specific time window.
This provides the carbon intensity (in gCO2/kWh) and the electricity generation mix (e.g., wind, solar, gas) during the job's execution.

#### Calculate Emissions

With the hardware specifications and environmental data in hand, GUILT calculates the energy usage and carbon emissions.

#### Update Records

Upon successful calculation, the job entry is updated with the computed energy, emissions, and generation mix data.
The job is then removed from `~/.guilt/unprocessed_jobs.json` and appended to the `~/.guilt/processed_jobs.json` file, making it available for reporting.
::
