---
title: Batch
description: A wrapper around SLURM's sbatch command to submit jobs with GUILT tracking
navigation:
  icon: i-lucide-send
---

## Usage

```bash [Terminal]
guilt batch <script>
```

Where `<script>` is the path to a SLURM batch script.

## Description

The GUILT `batch` command is a wrapper around SLURM's `sbatch` command that registers jobs with GUILT tracking.
When you would have used `sbatch` to submit a job, you should now use `guilt batch`.

## How it works

When you submit a job using `guilt batch`, GUILT will do the following steps:

::steps{level=4}
#### Parse the batch script for directives

GUILT will parse the directives at the top of the given script.

For example, the below script:

```bash [Terminal]
#!/bin/bash --login

#SBATCH --job-name=testing_guilt
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=0:02:00
#SBATCH --constraint=amd
#GUILT --cpu-profile=AMD EPYC 9654

echo "hello world"
```

Will result in the following directives being parsed:

| Directive | Value |
|---|---|
| `#SBATCH --nodes` | `1` | 
| `#SBATCH --tasks-per-node` | `1` |
| `#SBATCH --cpus-per-task` | `1` |
| `#SBATCH --time` | `0:02:00` |
| `#GUILT --cpu-profile` | `AMD EPYC 9654` |

You may notice that aswell as the standard SLURM directives, there is also a `#GUILT` directive.
These are custom directives that GUILT uses to specify additional information.

These parsed directives are then used to print an estimate of the job's emissions.

It should be noted that the `cpu-profile` directive is optional, and if it is not present GUILT will guess it using the Profile Resolution Policy.

#### Submit the job to SLURM

After parsing the directives, GUILT will submit the job to SLURM using the `sbatch` command in the background.

```bash [Terminal]
sbatch script.sh --parsable
```

GUILT will then capture the output of this command to get the job id of the submitted job.

#### Register the job in GUILT directory

GUILT will then register the job in the GUILT directory by adding it to the list of unprocessed jobs.

For example, if you submitted a job with id "12345" and you didnt provide a `cpu-profile` directive, the following entry would be added to the unprocessed jobs list:

```json [~/.guilt/unprocessed_jobs.json]
{
  "job_id": "12345",
  "cpu_profile_resolution_data": "None"
}
```
