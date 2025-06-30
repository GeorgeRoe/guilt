from guilt.models.carbon_intensity_time_segment import CarbonIntensityTimeSegment
from dataclasses import dataclass

@dataclass
class CarbonIntensityForecastResult:
  region_id: int
  short_name: str
  postcode: str
  segments: list[CarbonIntensityTimeSegment]