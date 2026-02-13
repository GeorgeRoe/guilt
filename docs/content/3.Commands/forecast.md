---
title: Forecast
description: Gives a forecast of carbon intensity for the near future
navigation:
  icon: i-lucide-trending-up
---

## Usage

```bash [Terminal]
guilt forecast
```

## Description

The GUILT `forecast` command provides users with a forecast of carbon intensity for the near future.
This information can be used to predict the optimum time to run jobs in order to minimize carbon emissions (Although GUILT does this automatically for you).

## How it works

::steps{level=4}
#### Query the Carbon Intensity API

GUILT queries the [Carbon Intensity API](https://carbonintensity.org.uk/) to retrieve the forcasted carbon intensity values for the near future.

#### Display the forecast

GUILT has two modes of output for the forecast data:

- **Terminal Output**: The default, uses ascii characters to display the forecast in the terminal.
- **Graphical Output**: If you are using [kitty](https://sw.kovidgoyal.net/kitty/), GUILT can display a graph directly in the terminal
::