from datetime import datetime, timedelta, timezone
import plotext as plt
import shutil
from guilt.services.ip_info import IpInfoService
from guilt.carbon_dioxide_forecast import CarbonDioxideForecast
from guilt.log import logger

def execute(_):
  ip_info = IpInfoService.fetchData()

  start = datetime.now(timezone.utc)
  end = start + timedelta(hours=12)
  
  logger.debug(f"Time range: {start} -> {end}")

  forecast = CarbonDioxideForecast(start, end, ip_info.postal)

  times_dt = [datetime.strptime(entry.from_time, "%Y-%m-%dT%H:%MZ") for entry in forecast.entries]
  values = [entry.intensity.forecast for entry in forecast.entries]

  start_time = times_dt[0]
  x = [(t - start_time).total_seconds() / 3600 for t in times_dt]
  labels = [t.strftime('%H:%M') for t in times_dt]

  terminal_size = shutil.get_terminal_size()
  width = terminal_size.columns
  height = max(5, int(width / 6))

  nth_tick = 2

  plt.clf()
  plt.plot_size(width, height)
  plt.theme('pro')
  plt.plot(x, values, marker='braille', label="CO₂ Intensity (gCO₂/kWh)")
  plt.title(f"{ip_info.postal} Carbon Intensity Forecast")
  plt.xlabel("Time (hours since start)")
  plt.ylabel("gCO₂/kWh")
  plt.xticks(x[::nth_tick], labels[::nth_tick])
  plt.show()

  print("\nBest Times:")

  best = sorted(forecast.entries, key=lambda x: x.intensity.forecast)[:5]
  for entry in best:
    time = datetime.strptime(entry.from_time, "%Y-%m-%dT%H:%MZ")
    print(f"{time.strftime('%a %d %b %H:%M')} → {entry.intensity.forecast} gCO₂/kWh")

def register_subparser(subparsers):
  subparser = subparsers.add_parser("forecast")
  subparser.set_defaults(function=execute)