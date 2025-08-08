from guilt.interfaces.command import CommandInterface
from guilt.interfaces.services.carbon_intensity_forecast import CarbonIntensityForecastServiceInterface
from guilt.interfaces.services.plotting import PlottingServiceInterface
from guilt.utility.plotting_context import PlottingContext
from guilt.mappers import map_to
from guilt.utility import ip_info
from datetime import datetime, timedelta, timezone

class ForecastCommand(CommandInterface):
  pass
  def __init__(
    self,
    carbon_intensity_forecast_service: CarbonIntensityForecastServiceInterface,
    plotting_service: PlottingServiceInterface
  ) -> None:
    self._carbon_intensity_forecast_service = carbon_intensity_forecast_service
    self._plotting_service = plotting_service

  @staticmethod
  def name() -> str:
    return "forecast"

  @staticmethod
  def configure_subparser(_) -> None:
    pass

  def execute(self, _) -> None:
    start = datetime.now(timezone.utc)
    end = start + timedelta(hours=24)
    
    forecast = self._carbon_intensity_forecast_service.get_forecast(start, end, ip_info.get().postal)

    intensity_data = map_to.time_series_data.from_carbon_intensity_forecast_result(forecast)

    with PlottingContext(self._plotting_service) as plot:
      plot.plot_time_series_data(
        intensity_data,
        title="Carbon Intensity Forecast",
        xlabel="Time",
        ylabel="gCO₂/kWh"
      )

    print("\nBest Times:")

    best = sorted(forecast.segments, key=lambda segment: segment.intensity)[:5]
    for segment in best:
      print(f"{segment.from_time.strftime('%a %d %b %H:%M')} → {segment.intensity} gCO₂/kWh")
