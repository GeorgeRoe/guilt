import httpx
import asyncio
from guilt.utility.safe_get import safe_get_string
from guilt.models.ip_info_result import IpInfoResult
from typing import Any

class IpInfoService:
  @classmethod
  def fetchData(cls) -> IpInfoResult:
    data = asyncio.run(cls.request())
    
    ip = safe_get_string(data, "ip")
    hostname = safe_get_string(data, "hostname")
    city = safe_get_string(data, "city")
    region = safe_get_string(data, "region")
    country = safe_get_string(data, "country")
    latitude, longitude = [float(value) for value in safe_get_string(data, "loc").split(",")]
    organisation = safe_get_string(data, "org")
    postal = safe_get_string(data, "postal")
    timezone = safe_get_string(data, "timezone")
    
    return IpInfoResult(
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

  @classmethod
  async def request(cls) -> dict[str, Any]:
    async with httpx.AsyncClient() as client:
      response = await client.get("http://ipinfo.io")

      if response.status_code == 200:
        return response.json()
      else:
        raise Exception(f"Error {response.status_code}: {response.text}")