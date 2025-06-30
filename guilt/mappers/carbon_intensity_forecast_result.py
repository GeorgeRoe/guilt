from typing import Any, cast
from guilt.utility.safe_get import safe_get_int, safe_get_string, safe_get_list
from guilt.models.carbon_intensity.forecast_result import CarbonIntensityForecastResult
from guilt.models.carbon_intensity.time_segment import CarbonIntensityTimeSegment
from guilt.mappers.carbon_intensity_time_segment import MapToCarbonIntensityTimeSegment

class MapToCarbonIntensityForecastResult:
  @classmethod
  def from_api_dict(cls, data: dict[str, Any]) -> CarbonIntensityForecastResult:
    region_id = safe_get_int(data, "regionid")
    short_name = safe_get_string(data, "shortname")
    postcode = safe_get_string(data, "postcode")
    segment_data = safe_get_list(data, "data")
    
    segments: list[CarbonIntensityTimeSegment] = []
    for item in segment_data:
      if isinstance(item, dict):
        segments.append(MapToCarbonIntensityTimeSegment.from_api_dict(cast(dict[str, Any], item)))
      else:
        raise ValueError("Items in time segment data should be dicts.")
      
    return CarbonIntensityForecastResult(region_id, short_name, postcode, segments)