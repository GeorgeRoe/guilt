from datetime import datetime

class CarbonIntensityTimeSegment:
  def __init__(
    self,
    from_time: datetime,
    to_time: datetime,
    intensity: float,
    index: str,
    generation_mix: dict[str, float]
  ) -> None:
    self.from_time = from_time
    self.to_time = to_time
    self.intensity = intensity
    self.index = index
    self.generation_mix = generation_mix
    
  def __repr__(self) -> str:
    return (
      f"CarbonIntensityTimeSegment(from_time={self.from_time}, "
      f"to_time={self.to_time}, "
      f"intensity={self.intensity}, "
      f"index={self.index}, "
      f"generation_mix={self.generation_mix})"
    )