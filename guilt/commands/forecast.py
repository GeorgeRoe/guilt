from guilt.interfaces.command import CommandInterface
from guilt.interfaces.services.ip_info import IpInfoServiceInterface
from guilt.interfaces.services.carbon_intensity_forecast import CarbonIntensityForecastServiceInterface
import shutil
from datetime import datetime, timedelta, timezone
import plotext

class ForecastCommand(CommandInterface):
  pass
  def __init__(
    self,
    ip_info_service: IpInfoServiceInterface,
    carbon_intensity_forecast_service: CarbonIntensityForecastServiceInterface
  ) -> None:
    self._ip_info_service = ip_info_service
    self._carbon_intensity_forecast_service = carbon_intensity_forecast_service

  @staticmethod
  def name() -> str:
    return "forecast"

  @staticmethod
  def configure_subparser(_) -> None:
    pass

  def execute(self, _) -> None:
    ip_info = self._ip_info_service.get_ip_info()

    start = datetime.now(timezone.utc)
    end = start + timedelta(hours=12)
    
    forecast = self._carbon_intensity_forecast_service.get_forecast(start, end, ip_info.postal)

    times_dt = [segment.from_time for segment in forecast.segments]
    values = [segment.intensity for segment in forecast.segments]

    start_time = times_dt[0]
    x = [(t - start_time).total_seconds() / 3600 for t in times_dt]
    labels = [t.strftime('%H:%M') for t in times_dt]

    terminal_size = shutil.get_terminal_size()
    width = terminal_size.columns
    height = max(5, int(width / 6))

    nth_tick = 2

    plotext.clf()
    plotext.plot_size(width, height)
    plotext.theme('pro')
    plotext.plot(x, values, marker='braille', label="CO₂ Intensity (gCO₂/kWh)")
    plotext.title(f"{ip_info.postal} Carbon Intensity Forecast")
    plotext.xlabel("Time (hours since start)")
    plotext.ylabel("gCO₂/kWh")
    plotext.xticks(x[::nth_tick], labels[::nth_tick])
    plotext.show()

    print("\nBest Times:")

    best = sorted(forecast.segments, key=lambda segment: segment.intensity)[:5]
    for segment in best:
      print(f"{segment.from_time.strftime('%a %d %b %H:%M')} → {segment.intensity} gCO₂/kWh")