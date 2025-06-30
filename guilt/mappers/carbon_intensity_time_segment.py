from typing import Any, cast
from datetime import datetime
from guilt.utility.safe_get import safe_get_string, safe_get_dict, safe_get_float, safe_get_list
from guilt.models.carbon_intensity.time_segment import CarbonIntensityTimeSegment

class MapToCarbonIntensityTimeSegment:
  @classmethod
  def from_api_dict(cls, data: dict[str, Any]) -> CarbonIntensityTimeSegment:
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
        
    return CarbonIntensityTimeSegment(from_time, to_time, intensity, index, generation_mix)