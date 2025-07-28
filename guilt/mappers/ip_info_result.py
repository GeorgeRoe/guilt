from guilt.models.ip_info_result import IpInfoResult
from guilt.types.json import Json
from guilt.utility.json_reader import JsonReader

class MapToIpInfoResult:
  @staticmethod
  def from_json(data: Json) -> IpInfoResult:
    data = JsonReader.expect_dict(data)
    
    ip = JsonReader.ensure_get_str(data, "ip")
    hostname = data.get("hostname")
    city = JsonReader.ensure_get_str(data, "city")
    region = JsonReader.ensure_get_str(data, "region")
    country = JsonReader.ensure_get_str(data, "country")
    latitude, longitude = [float(value) for value in JsonReader.ensure_get_str(data, "loc").split(",")]
    organisation = JsonReader.ensure_get_str(data, "org")
    postal = JsonReader.ensure_get_str(data, "postal")
    timezone = JsonReader.ensure_get_str(data, "timezone")
    
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