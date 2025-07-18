import respx
import httpx
import pytest
from guilt.interfaces.services.ip_info import IpInfoServiceInterface
from guilt.services.ip_info import IpInfoService
from guilt.models.ip_info_result import IpInfoResult
from guilt.dependencies.injector import DependencyInjector
from guilt.types.json import Json

@respx.mock
def test_get_forecast_success() -> None:
  di = DependencyInjector()
  di.bind(IpInfoServiceInterface, IpInfoService)
  ip_info_service = di.resolve(IpInfoServiceInterface) # type: ignore[type-abstract]
  
  url = "http://ipinfo.io"
  
  response: dict[str, Json] = {
    "ip": "1.1.1.1",
    "hostname": "",
    "city": "Daresbury",
    "region": "England",
    "country": "GB",
    "loc": "53.34442528628549, -2.6402926735529935",
    "org": "STFC",
    "postal": "WA4",
    "timezone": "Europe/London",
    "readme": "https://ipinfo.io/missingauth"
  }
  
  respx.get(url).mock(return_value=httpx.Response(200, json=response))
  
  result = ip_info_service.get_ip_info()
  
  assert isinstance(result, IpInfoResult)
  
@respx.mock
def test_get_forecast_raises() -> None:
  di = DependencyInjector()
  di.bind(IpInfoServiceInterface, IpInfoService)
  ip_info_service = di.resolve(IpInfoServiceInterface) # type: ignore[type-abstract]
  
  url = "http://ipinfo.io"
  
  respx.get(url).mock(return_value=httpx.Response(404))
  
  with pytest.raises(Exception):
    ip_info_service.get_ip_info()