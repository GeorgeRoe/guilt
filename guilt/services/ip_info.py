import httpx
import asyncio
from guilt.utility.safe_get import safe_get_string
from typing import Any

class IpInfoResult:
  def __init__(self, ip: str, hostname: str, city: str, region: str, country: str, latitude: float, longitude: float, organisation: str, postal: str, timezone: str):
    self.ip = ip
    self.hostname = hostname
    self.city = city
    self.region = region
    self.country = country
    self.latitude = latitude
    self.longitude = longitude
    self.organisation = organisation
    self.postal = postal
    self.timezone = timezone
  
  @classmethod
  def fromDict(cls, data: dict[str, Any]):
    ip = safe_get_string(data, "ip")
    hostname = safe_get_string(data, "hostname")
    city = safe_get_string(data, "city")
    region = safe_get_string(data, "region")
    country = safe_get_string(data, "country")
    latitude, longitude = [float(value) for value in safe_get_string(data, "loc").split(",")]
    organisation = safe_get_string(data, "org")
    postal = safe_get_string(data, "postal")
    timezone = safe_get_string(data, "timezone")
    
    return cls(
      ip,
      hostname,
      city,
      region,
      country,
      latitude,
      longitude,
      organisation,
      postal,
      timezone
    )

class IpInfoService:
  @classmethod
  def fetchData(cls) -> IpInfoResult:
    return IpInfoResult.fromDict(asyncio.run(cls.request()))

  @classmethod
  async def request(cls) -> dict[str, Any]:
    async with httpx.AsyncClient() as client:
      response = await client.get("http://ipinfo.io")

      if response.status_code == 200:
        return response.json()
      else:
        raise Exception(f"Error {response.status_code}: {response.text}")