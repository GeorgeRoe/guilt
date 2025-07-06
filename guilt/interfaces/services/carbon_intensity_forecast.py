from abc import ABC, abstractmethod
from datetime import datetime
from guilt.models.carbon_intensity_forecast_result import CarbonIntensityForecastResult

class CarbonIntensityForecastServiceInterface(ABC):
  @abstractmethod
  def get_forecast(self, from_time: datetime, to_time: datetime, postcode: str) -> CarbonIntensityForecastResult:
    pass