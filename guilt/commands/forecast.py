from datetime import datetime, timedelta, timezone
import plotext as plt
import shutil
from guilt.log import logger
from argparse import Namespace
from guilt.utility.subparser_adder import SubparserAdder
from guilt.dependencies.manager import dependency_manager

ip_info_repository = dependency_manager.repository.ip_info
carbon_intensity_forecast_repository = dependency_manager.repository.carbon_intensity_forecast

def execute(args: Namespace):
  ip_info = ip_info_repository.fetch_data()

  start = datetime.now(timezone.utc)
  end = start + timedelta(hours=12)
  
  logger.debug(f"Time range: {start} -> {end}")

  forecast = carbon_intensity_forecast_repository.fetch_data(start, end, ip_info.postal)

  times_dt = [segment.from_time for segment in forecast.segments]
  values = [segment.intensity for segment in forecast.segments]

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

  best = sorted(forecast.segments, key=lambda segment: segment.intensity)[:5]
  for segment in best:
    print(f"{segment.from_time.strftime('%a %d %b %H:%M')} → {segment.intensity} gCO₂/kWh")

def register_subparser(subparsers: SubparserAdder):
  subparser = subparsers.add_parser("forecast")
  subparser.set_defaults(function=execute)