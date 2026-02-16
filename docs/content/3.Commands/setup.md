---
title: Setup
description: Prepares GUILT for use on your HPC system
navigation:
  icon: i-lucide-upload
---

## Usage

```bash [Terminal]
guilt setup
```

## Description

The GUILT `setup` command initializes the necessary configuration files in the `~/.guilt/` directory.
If your system is recognised, it will automatically generate relevant configuration files.

## How it works

::steps{level=4}
#### System Detection

GUILT has a list of objects that contain three things:

- A function that checks various system parameters (e.g., environment variables, command outputs) to determine if the current system matches a known HPC cluster.
- A set of CPU Profiles that are relevant to that system.
- A profile resolution policy for the system. These are optional and might not yet exist for your system, but they will be added over time.

When you run `guilt setup`, GUILT iterates through this list and executes the detection function for each object.

#### Configuration Generation

If a function detects a match, GUILT then pushes the associated configurations to the `~/.guilt/` directory.

#### Manual Setup

If your system was not automatically detected, the user must manually set up the configuration files themselves.
::