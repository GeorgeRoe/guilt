# GUILT

Green Usage Impact Logging Tool allows users to keep track of their carbon emissions whilst working with SLURM.

## Installation

To install GUILT (on x86_64 linux) you can simply use the `install.sh` script:

```bash
curl -sSL https://raw.githubusercontent.com/GeorgeRoe/guilt/main/install-guilt.sh | sh
```

For a custom install, GUILT binaries can be found in the releases section of the repository.

## Getting Started

Once you have installed GUILT there a few commands you should run:

```sh
# setup guilt config and data
guilt setup

# modify your cpu profiles config to match the hardware of your machines
vim ~/.guilt/cpu_profiles.json

# add all historical slurm jobs to the list of jobs to process for the report
# this command will assume jobs were ran on the default cpu_profile
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