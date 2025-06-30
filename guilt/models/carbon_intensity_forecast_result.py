from guilt.models.carbon_intensity_time_segment import CarbonIntensityTimeSegment

class CarbonIntensityForecastResult:
  def __init__(
    self,
    region_id: int,
    short_name: str,
    postcode: str,
    segments: list[CarbonIntensityTimeSegment]
  ) -> None:
    self.region_id = region_id
    self.short_name = short_name
    self.postcode = postcode
    self.segments = segments
    
  def __repr__(self) -> str:
    return (
      f"CarbonIntensityForecastResult(region_id={self.region_id}, "
      f"short_name={self.short_name}, "
      f"postcode={self.postcode}, "
      f"segments={self.segments})"
    )