# GUILT

Green Usage Impact Logging Tool allows users to keep track of their carbon emissions whilst working with SLURM.

## Installation

When installing GUILT, compiling from source is recommended to reduce compatibility issues.
This repo provides shell scripts to improve the installation process, please ensure that
you have read these scripts before you execute them.

You can use the `install-compile.sh` shell script to automatically compile and install GUILT.
You must have `cargo` installed for this script to work, if you dont you can set it up in a
manner of seconds by following the instructions at https://rustup.rs/.

```bash
cargo version # must not error
curl -sSL https://raw.githubusercontent.com/GeorgeRoe/guilt/main/install-compile.sh | sh
```

If you want to avoid installing rust on your machine, you can attempt to install from a
release using `install-release.sh`. This should work for linux users on x86 and ARM systems.
Be warned, this project relies on openssl and there are sometimes incompatibility problems
between the openssl version used for compilation and your systems openssl versions. Again,
it is heavily recommended to compile from source.

```bash
curl -sSL https://raw.githubusercontent.com/GeorgeRoe/guilt/main/install-release.sh | sh
```

## Getting Started

Once you have installed GUILT there a few commands you should run:

```sh
# setup guilt config and data
guilt setup

# modify your cpu profiles config to match the hardware of your machines
# [ { "name": "profile name", "cores": 1, "tdp": 10 }]
vim ~/.guilt/cpu_profiles.json

# add all historical slurm jobs to the list of jobs to process for the report
# this command will assume jobs were ran on the default cpu_profile:w

guilt backfill

# processes all the jobs to calculate their emissions
guilt process

# show a report of your historical usage
guilt report
```

## Usage

### Setup

The `setup` command will create the `~/.guilt` folder and generate default config and data files.

```sh
guilt setup
```

### Teardown

The `teardown` command will delete the `~/.guilt` folder and its contents.

```sh
guilt teardown
```

### Config

The `config` command allows you to modify and update config records, such as CPU profiles.

```sh
# opens an interactive input for creation of a new cpu profile
guilt config add cpu_profile
```

### Forecast

The `forecast` command renders a graph to the terminal displaying how many grams of CO2 will be released per kWh for the foreseeable future.

```sh
guilt forecast
```

### Batch

The `batch` command is now your replacement for the `sbatch` command, by using this GUILT will add the job info to a list of "unprocessed" jobs. GUILT will also read the file for extra parameters, lines starting with "#GUILT" will store information such as what cpu profile this job is using.

```sh
guilt batch script.sh
```

### Process

The `process` command collects data about each job in the "unprocesssed" jobs list to calculate carbon emissions. This is achieved by using `sacct` and calling the [Carbon Intensity API](https://carbonintensity.org.uk/). After this, the jobs will be added to a list of "processed" jobs, which will be the source of data for reports.

```sh
guilt process
```

### Report

The `report` command will display an overview of your carbon emissions.

```sh
guilt report
```

### Backfill

The `backfill` command uses data from `sacct` to estimate your historical usage by assuming that all previous jobs that were ran with `sbatch` used the configured default cpu profile. This command should only need to be ran once when you first install `guilt`.

```sh
guilt backfill
```

### Friends

The `friends` command uses data from `getent passwd` to find other people using GUILT on the machine.

```sh
guilt friends
```