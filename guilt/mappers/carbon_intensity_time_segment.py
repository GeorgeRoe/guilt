from datetime import datetime
from guilt.types.json import Json
from guilt.utility.json_reader import JsonReader
from guilt.models.carbon_intensity_time_segment import CarbonIntensityTimeSegment

class MapToCarbonIntensityTimeSegment:
  @staticmethod
  def from_json(data: Json) -> CarbonIntensityTimeSegment:
    data = JsonReader.expect_dict(data)
    
    from_time = datetime.fromisoformat(JsonReader.ensure_get_str(data, "from").replace("Z", ""))
    to_time = datetime.fromisoformat(JsonReader.ensure_get_str(data, "to").replace("Z", ""))
    
    intensity_data = JsonReader.ensure_get_dict(data, "intensity")
    intensity = float(JsonReader.ensure_get_number(intensity_data, "forecast"))
    index = JsonReader.ensure_get_str(intensity_data, "index")
    
    generation_mix_array = JsonReader.ensure_get_list(data, "generationmix")
    generation_mix: dict[str, float] = {}
    for item in generation_mix_array:
      item_data = JsonReader.expect_dict(item)
      fuel = JsonReader.ensure_get_str(item_data, "fuel")
      percent = float(JsonReader.ensure_get_number(item_data, "perc"))
      generation_mix[fuel] = percent
  
    return CarbonIntensityTimeSegment(from_time, to_time, intensity, index, generation_mix)