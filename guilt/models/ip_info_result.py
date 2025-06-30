from dataclasses import dataclass

@dataclass
class IpInfoResult:
  ip: str
  hostname: str
  city: str
  region: str
  country: str
  latitude: float
  longitude: float
  organisation: str
  postal: str
  timezone: str