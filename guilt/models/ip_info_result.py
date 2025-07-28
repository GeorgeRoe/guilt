from dataclasses import dataclass
from typing import Optional

@dataclass
class IpInfoResult:
  ip: str
  hostname: Optional[str]
  city: str
  region: str
  country: str
  latitude: float
  longitude: float
  organisation: str
  postal: str
  timezone: str