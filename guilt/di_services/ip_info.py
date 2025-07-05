from guilt.interfaces.services.ip_info import IpInfoServiceInterface
from guilt.models.ip_info_result import IpInfoResult
from guilt.mappers import map_to
import asyncio
import httpx
from typing import Any

class IpInfoService(IpInfoServiceInterface):
  def get_ip_info(self) -> IpInfoResult:
    return map_to.ip_info_result.from_api_dict(asyncio.run(self._api_fetch()))

  async def _api_fetch(self) -> dict[str, Any]:
    async with httpx.AsyncClient() as client:
      response = await client.get("http://ipinfo.io")

      if response.status_code == 200:
        return response.json()
      else:
        raise Exception(f"Error {response.status_code}: {response.text}")