from typing import Any
from guilt.models.ip_info_result import IpInfoResult
from guilt.utility.safe_get import safe_get_string

class MapToIpInfoResult:
  @classmethod
  def from_api_dict(cls, data: dict[str, Any]) -> IpInfoResult:
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