from datetime import datetime, timedelta, UTC
import plotext as plt
import shutil
import httpx
import asyncio
import argparse

async def get_ip_info():
  async with httpx.AsyncClient() as client:
    response = await client.get("http://ipinfo.io")

    if response.status_code == 200:
      return response.json()
    else:
      raise Exception(f"Error {response.status_code}: {response.text}")
    
async def get_forecast(from_dt, to_dt, postcode):
  from_str = from_dt.strftime('%Y-%m-%dT%H:%MZ')
  to_str = to_dt.strftime('%Y-%m-%dT%H:%MZ')

  async with httpx.AsyncClient() as client:
    response = await client.get(f"https://api.carbonintensity.org.uk/regional/intensity/{from_str}/{to_str}/postcode/{postcode}")

    if response.status_code == 200:
      return response.json()
    else:
      raise Exception(f"Error {response.status_code}: {response.text}")

def plot_co2_forecast_limited(forecast_data, aspect_ratio=6):
  # Convert ISO timestamps to datetime objects
  times_dt = [datetime.strptime(entry['from'], "%Y-%m-%dT%H:%MZ") for entry in forecast_data]
  values = [entry['intensity']['forecast'] for entry in forecast_data]

  # Use time since first point in hours as x-axis
  start_time = times_dt[0]
  x = [(t - start_time).total_seconds() / 3600 for t in times_dt]
  labels = [t.strftime('%d %H:%M') for t in times_dt]  # For nicer x-tick labels

  terminal_size = shutil.get_terminal_size()
  width = terminal_size.columns
  height = max(5, int(width / aspect_ratio))

  plt.clf()
  plt.plot_size(width, height)
  plt.theme('clear')
  plt.plot(x, values, marker='braille', label="CO₂ Intensity (gCO₂/kWh)")
  plt.title("UK Carbon Intensity Forecast")
  plt.xlabel("Time (hours since start)")
  plt.ylabel("gCO₂/kWh")
  plt.xticks(x[::4], labels[::4])
  plt.show()

def main():
  parser = argparse.ArgumentParser(
    description="GUILT: Green Usage Impact Logging Tool"
  )

  subparsers = parser.add_subparsers(dest="command", required=True)

  forecast_parser = subparsers.add_parser("forecast")

  config_parser = subparsers.add_parser("config")

  args = parser.parse_args()

  if args.command == "forecast":
    ip_data = asyncio.run(get_ip_info())
    postal = ip_data['postal']

    start = datetime.now(UTC)
    end = start + timedelta(hours=48)

    forecast_data = asyncio.run(get_forecast(start, end, postal))['data']

    forecast_results = sorted(forecast_data['data'], key=lambda x: x['from'])

    plot_co2_forecast_limited(forecast_results)

    best = sorted(forecast_results, key=lambda x: x['intensity']['forecast'])[:5]
    for entry in best:
      time = datetime.strptime(entry['from'], "%Y-%m-%dT%H:%MZ")
      print(f"{time.strftime('%a %d %b %H:%M')} → {entry['intensity']['forecast']} gCO₂/kWh")
  elif args.command == "config":
    print("CONFIG! WIP")