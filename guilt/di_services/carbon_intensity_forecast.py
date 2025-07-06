from guilt.interfaces.services.carbon_intensity_forecast import CarbonIntensityForecastServiceInterface
from guilt.models.carbon_intensity_forecast_result import CarbonIntensityForecastResult
from guilt.types.json import Json
from guilt.mappers import map_to
from datetime import datetime
import httpx
import asyncio

class CarbonIntensityForecastService(CarbonIntensityForecastServiceInterface):
  def get_forecast(self, from_time: datetime, to_time: datetime, postcode: str) -> CarbonIntensityForecastResult:
    return map_to.carbon_intensity_forecast_result.from_json(
      asyncio.run(self._api_fetch(from_time, to_time, postcode))
    )
  
  async def _api_fetch(self, from_time: datetime, to_time: datetime, postcode: str) -> Json:
    time_format = "%Y-%m-%dT%H:%MZ"
    from_str = from_time.strftime(time_format)
    to_str = to_time.strftime(time_format)
    url = f"https://api.carbonintensity.org.uk/regional/intensity/{from_str}/{to_str}/postcode/{postcode}"
  
    async with httpx.AsyncClient() as client:
      response = await client.get(url)

    if response.status_code == 200:
      return response.json()
    else:
      raise Exception(f"Error {response.status_code}: {response.text}")