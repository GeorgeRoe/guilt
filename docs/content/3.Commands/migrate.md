---
title: Migrate
description: Migrates existing data from older GUILT formats to the format of the version being used
navigation:
  icon: i-lucide-git-branch-plus
---

## Usage

```bash [Terminal]
guilt migrate
```

## Description

The GUILT `migrate` command is used to migrate data from older versions of GUILT to the current version.
This ensures that your historical job data and configuration remain compatible as GUILT evolves.

## How it works

::steps{level=4}
#### Store a backup

GUILT will automatically create a backup of your existing data before performing any migration.
This backup is stored in your home directory as `~/.guilt.bak`.

#### Check for and run updates

GUILT stores a list of migration objects that can both:

- Detect whether they are applicable to the current data (In later versions of GUILT, a `last_written_version` field is added to the data, making it easy to determine which migrations need to be applied)
- Perform the necessary transformations to update the data to the new format

These are applied in sequence (if applicable) until the data is fully migrated to the latest format.
::
