from datetime import datetime
from typing import Any, cast
import httpx
import asyncio
from guilt.log import logger
from guilt.utility.safe_get import safe_get_dict
from guilt.models.carbon_intensity_forecast_result import CarbonIntensityForecastResult
from guilt.mappers.carbon_intensity_forecast_result import MapToCarbonIntensityForecastResult

class CarbonIntensityForecastService:
  @classmethod
  def fetch_data(cls, from_time: datetime, to_time: datetime, postcode: str) -> CarbonIntensityForecastResult:
    return MapToCarbonIntensityForecastResult.from_api_dict(
      asyncio.run(CarbonIntensityForecastService.request(from_time, to_time, postcode))
    )
  
  @classmethod
  async def request(cls, from_time: datetime, to_time: datetime, postcode: str) -> dict[str, Any]:
    time_format = "%Y-%m-%dT%H:%MZ"
    from_str = from_time.strftime(time_format)
    to_str = to_time.strftime(time_format)
    url = f"https://api.carbonintensity.org.uk/regional/intensity/{from_str}/{to_str}/postcode/{postcode}"
    
    logger.debug(f"Sending request to: {url}")
    async with httpx.AsyncClient() as client:
      response = await client.get(url)

    if response.status_code == 200:
      logger.debug("Received successful response from carbon intensity API")
      data = cast(dict[str, Any], response.json())
      return safe_get_dict(data, "data")
    else:
      logger.error(f"API request failed: {response.status_code} {response.text}")
      raise Exception(f"Error {response.status_code}: {response.text}")