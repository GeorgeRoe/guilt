from guilt.models.lazy_ip_info_result import LazyIpInfoResult
from guilt.types.json import Json
from guilt.utility import json_reader
from typing import Optional
import asyncio
import httpx

IP_INFO_URL = "http://ipinfo.io"

async def _api_fetch() -> Json:
  async with httpx.AsyncClient() as client:
    response = await client.get(IP_INFO_URL)

    if response.status_code == 200:
      return response.json()
    else:
      raise Exception(f"Error {response.status_code}: {response.text}")

def get() -> LazyIpInfoResult:
  return LazyIpInfoResult(json_reader.expect_dict(asyncio.run(_api_fetch())))