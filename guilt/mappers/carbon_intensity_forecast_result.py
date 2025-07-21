from guilt.models.carbon_intensity_forecast_result import CarbonIntensityForecastResult
from guilt.mappers.carbon_intensity_time_segment import MapToCarbonIntensityTimeSegment
from guilt.types.json import Json
from guilt.utility.json_reader import JsonReader

class MapToCarbonIntensityForecastResult:
  @staticmethod
  def from_json(data: Json) -> CarbonIntensityForecastResult:
    data = JsonReader.expect_dict(data)
    data = JsonReader.ensure_get_dict(data, "data")
    
    region_id = JsonReader.ensure_get_int(data, "regionid")
    short_name = JsonReader.ensure_get_str(data, "shortname")
    postcode = JsonReader.ensure_get_str(data, "postcode")
    segment_data = JsonReader.ensure_get_list(data, "data")
    
    segments = [MapToCarbonIntensityTimeSegment.from_json(item) for item in segment_data]
    
    return CarbonIntensityForecastResult(region_id, short_name, postcode, segments)