from guilt.models.carbon_intensity_forecast_result import CarbonIntensityForecastResult
from guilt.utility.time_series_data import TimeSeriesData

class MapToTimeSeriesData:
  @staticmethod
  def from_carbon_intensity_forecast_result(forecast: CarbonIntensityForecastResult) -> TimeSeriesData:
    return TimeSeriesData({
      **{
        segment.from_time: segment.intensity for segment in forecast.segments
      },
      forecast.segments[-1].to_time: forecast.segments[-1].intensity
    })