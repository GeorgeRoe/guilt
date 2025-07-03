import httpx
import asyncio
from guilt.models.ip_info_result import IpInfoResult
from guilt.mappers.ip_info_result import MapToIpInfoResult
from typing import Any

class IpInfoRepository:
  def fetch_data(self) -> IpInfoResult:
    return MapToIpInfoResult.from_api_dict(asyncio.run(self.request()))

  async def request(self) -> dict[str, Any]:
    async with httpx.AsyncClient() as client:
      response = await client.get("http://ipinfo.io")

      if response.status_code == 200:
        return response.json()
      else:
        raise Exception(f"Error {response.status_code}: {response.text}")