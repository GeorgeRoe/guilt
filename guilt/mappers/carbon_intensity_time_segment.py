from datetime import datetime
from guilt.types.json import Json
from guilt.utility import json_reader
from guilt.models.carbon_intensity_time_segment import CarbonIntensityTimeSegment

class MapToCarbonIntensityTimeSegment:
  @staticmethod
  def from_json(data: Json) -> CarbonIntensityTimeSegment:
    data = json_reader.expect_dict(data)
    
    from_time = datetime.fromisoformat(json_reader.ensure_get_str(data, "from").replace("Z", ""))
    to_time = datetime.fromisoformat(json_reader.ensure_get_str(data, "to").replace("Z", ""))
    
    intensity_data = json_reader.ensure_get_dict(data, "intensity")
    intensity = float(json_reader.ensure_get_number(intensity_data, "forecast"))
    index = json_reader.ensure_get_str(intensity_data, "index")
    
    generation_mix_array = json_reader.ensure_get_list(data, "generationmix")
    generation_mix: dict[str, float] = {}
    for item in generation_mix_array:
      item_data = json_reader.expect_dict(item)
      fuel = json_reader.ensure_get_str(item_data, "fuel")
      percent = float(json_reader.ensure_get_number(item_data, "perc"))
      generation_mix[fuel] = percent
  
    return CarbonIntensityTimeSegment(from_time, to_time, intensity, index, generation_mix)