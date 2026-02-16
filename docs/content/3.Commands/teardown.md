---
title: Teardown
description: Removes all GUILT-related data from your HPC system
navigation:
  icon: i-lucide-trash
---

## Usage

```bash [Terminal]
guilt teardown 
```

## Description

The GUILT `teardown` command removes all GUILT-related data from your HPC system.
This data cannot be recovered, so use this command with caution.

## How it works

::steps{level=4}
#### Get User Confirmation

GUILT will prompt the user to confirm that they want to proceed with the teardown process, as this action is irreversible.

#### Remove GUILT Data

The `~/.guilt/` directory and all its contents will be deleted, effectively removing all GUILT-related data from the system.
::