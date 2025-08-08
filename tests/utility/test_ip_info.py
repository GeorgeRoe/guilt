import respx
import httpx
import pytest
from guilt.utility import ip_info
from guilt.models.lazy_ip_info_result import LazyIpInfoResult
from guilt.dependencies.injector import DependencyInjector
from guilt.types.json import Json

@respx.mock
def test_get_forecast_success() -> None:
  ip = "1.1.1.1"
  hostname = ""
  city = "Daresbury"
  region = "England"
  country = "GB"
  loc = "53.34442528628549, -2.6402926735529935"
  org = "STFC"
  postal = "WA4"
  timezone = "Europe/London"

  response: dict[str, Json] = {
    "ip": ip,
    "hostname": hostname,
    "city": city,
    "region": region,
    "country": country,
    "loc": loc,
    "org": org,
    "postal": postal,
    "timezone": timezone
  }
  
  respx.get(ip_info.IP_INFO_URL).mock(return_value=httpx.Response(200, json=response))
  
  result = ip_info.get()
  
  assert isinstance(result, LazyIpInfoResult)

  assert result.ip == ip
  assert result.hostname == hostname
  assert result.city == city
  assert result.region == region
  assert result.country == country
  assert result.loc == loc
  assert result.org == org
  assert result.postal == postal
  assert result.timezone == timezone
  
@respx.mock
def test_get_forecast_raises() -> None:
  respx.get(ip_info.IP_INFO_URL).mock(return_value=httpx.Response(404))
  
  with pytest.raises(Exception):
    ip_info.get()