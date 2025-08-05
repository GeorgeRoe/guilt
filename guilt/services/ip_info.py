from guilt.interfaces.services.ip_info import IpInfoServiceInterface
from guilt.models.lazy_ip_info_result import LazyIpInfoResult
from guilt.types.json import Json
from guilt.utility.json_reader import JsonReader
from typing import Optional
import asyncio
import httpx

class IpInfoService(IpInfoServiceInterface):
  def __init__(self) -> None:
    self._cache: Optional[LazyIpInfoResult] = None

  def get_ip_info(self) -> LazyIpInfoResult:
    if self._cache is None:
      self._cache = LazyIpInfoResult(JsonReader.expect_dict(asyncio.run(self._api_fetch())))
    return self._cache

  async def _api_fetch(self) -> Json:
    async with httpx.AsyncClient() as client:
      response = await client.get("http://ipinfo.io")

      if response.status_code == 200:
        return response.json()
      else:
        raise Exception(f"Error {response.status_code}: {response.text}")