from datetime import datetime
from typing import Any, cast
import httpx
import asyncio
from guilt.log import logger
from guilt.utility.safe_get import safe_get_dict, safe_get_int, safe_get_string, safe_get_float, safe_get_list

class CarbonIntensityTimeSegment:
  def __init__(self, from_time: datetime, to_time: datetime, intensity: float, index: str, generation_mix: dict[str, float]) -> None:
    self.from_time = from_time
    self.to_time = to_time
    self.intensity = intensity
    self.index = index
    self.generation_mix = generation_mix
    
  @classmethod
  def from_dict(cls, data: dict[str, Any]) -> "CarbonIntensityTimeSegment":
    from_str = safe_get_string(data, "from")
    to_str = safe_get_string(data, "to")
    
    from_time = datetime.fromisoformat(from_str.replace("Z", "+00:00"))
    to_time = datetime.fromisoformat(to_str.replace("Z", "+00:00"))
    
    intensity_data = safe_get_dict(data, "intensity")
    intensity = safe_get_float(intensity_data, "forecast")
    index = safe_get_string(intensity_data, "index")
    
    generation_mix_array = safe_get_list(data, "generationmix")
    generation_mix: dict[str, float] = {}
    for item in generation_mix_array:
      if isinstance(item, dict):
        item_values = cast(dict[str, Any], item)
        fuel = safe_get_string(item_values, "fuel")
        percent = safe_get_float(item_values, "perc")
        generation_mix[fuel] = percent
      else:
        raise ValueError("Each item in generation mix array should be a dict.")
        
    return cls(from_time, to_time, intensity, index, generation_mix)
  
  def __repr__(self) -> str:
    return (
      f"CarbonIntensityTimeSegment(from_time={self.from_time}, "
      f"to_time={self.to_time}, "
      f"intensity={self.intensity}, "
      f"index={self.index}, "
      f"generation_mix={self.generation_mix})"
    )    

class CarbonIntensityForecastResult:
  def __init__(self, region_id: int, short_name: str, postcode: str, segments: list[CarbonIntensityTimeSegment]) -> None:
    self.region_id = region_id
    self.short_name = short_name
    self.postcode = postcode
    self.segments = segments

  @classmethod
  def from_dict(cls, data: dict[str, Any]) -> "CarbonIntensityForecastResult":
    region_id = safe_get_int(data, "regionid")
    short_name = safe_get_string(data, "shortname")
    postcode = safe_get_string(data, "postcode")
    segment_data = safe_get_list(data, "data")
    
    segments: list[CarbonIntensityTimeSegment] = []
    for item in segment_data:
      if isinstance(item, dict):
        segments.append(CarbonIntensityTimeSegment.from_dict(cast(dict[str, Any], item)))
      else:
        raise ValueError("Items in time segment data should be dicts.")
      
    return cls(region_id, short_name, postcode, segments)
  
  def __repr__(self) -> str:
    return (
      f"CarbonIntensityForecastResult(region_id={self.region_id}, "
      f"short_name={self.short_name}, "
      f"postcode={self.postcode}, "
      f"segments={self.segments})"
    )

class CarbonIntensityForecastService:
  @classmethod
  def fetch_data(cls, from_time: datetime, to_time: datetime, postcode: str) -> CarbonIntensityForecastResult:
    return CarbonIntensityForecastResult.from_dict(
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