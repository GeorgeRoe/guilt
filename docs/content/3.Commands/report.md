---
title: Report
description: Generates a report from processed jobs data
navigation:
  icon: i-lucide-file-text
---

## Usage

```bash [Terminal]
guilt report --format <format>
```

Where format can be one of:

- `pdf` - Generates a PDF in the current working directory
- `terminal` (Default) - Prints the report directly into the terminal

## Description

The GUILT `report` command generates a comprehensive report based on the data from the `processed_jobs.json` file.

## How it works

The `report` command reads the list of processed jobs from `~/.guilt/processed_jobs.json` and compiles a report including various metrics.