from guilt.models.carbon_intensity_forecast_result import CarbonIntensityForecastResult
from guilt.mappers.carbon_intensity_time_segment import MapToCarbonIntensityTimeSegment
from guilt.types.json import Json
from guilt.utility import json_reader

class MapToCarbonIntensityForecastResult:
  @staticmethod
  def from_json(data: Json) -> CarbonIntensityForecastResult:
    data = json_reader.expect_dict(data)
    data = json_reader.ensure_get_dict(data, "data")
    
    region_id = json_reader.ensure_get_int(data, "regionid")
    short_name = json_reader.ensure_get_str(data, "shortname")
    postcode = json_reader.ensure_get_str(data, "postcode")
    segment_data = json_reader.ensure_get_list(data, "data")
    
    segments = [MapToCarbonIntensityTimeSegment.from_json(item) for item in segment_data]
    
    return CarbonIntensityForecastResult(region_id, short_name, postcode, segments)