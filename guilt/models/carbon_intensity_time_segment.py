from datetime import datetime
from dataclasses import dataclass

@dataclass
class CarbonIntensityTimeSegment:
  from_time: datetime
  to_time: datetime
  intensity: float
  index: str
  generation_mix: dict[str, float]