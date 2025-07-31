from enum import Enum
from guilt.types.json import Json
from guilt.models.location import Location

class _IpInfoJsonField(Enum):
  IP = "ip"
  HOSTNAME = "hostname"
  CITY = "city"
  REGION = "region"
  COUNTRY = "country"
  LOCATION = "loc"
  ORGANISATION = "org"
  POSTAL = "postal"
  TIMEZONE = "timezone"

def _get_field_value(data: dict[str, Json], field: _IpInfoJsonField) -> str:
  if field.value not in data:
    raise ValueError(f"Missing expected field: {field.value}")
  return str(data[field.value])

def get_ip(data: dict[str, Json]) -> str:
  return _get_field_value(data, _IpInfoJsonField.IP)

def get_hostname(data: dict[str, Json]) -> str:
  return _get_field_value(data, _IpInfoJsonField.HOSTNAME)

def get_city(data: dict[str, Json]) -> str:
  return _get_field_value(data, _IpInfoJsonField.CITY)

def get_region(data: dict[str, Json]) -> str:
  return _get_field_value(data, _IpInfoJsonField.REGION)

def get_country(data: dict[str, Json]) -> str:
  return _get_field_value(data, _IpInfoJsonField.COUNTRY)

def get_location(data: dict[str, Json]) -> Location:
  loc_str = _get_field_value(data, _IpInfoJsonField.LOCATION)
  try:
    latitude, longitude = map(float, loc_str.split(","))
    return Location(latitude=latitude, longitude=longitude)
  except ValueError:
    raise ValueError(f"Invalid location format: {loc_str}")
  
def get_organisation(data: dict[str, Json]) -> str:
  return _get_field_value(data, _IpInfoJsonField.ORGANISATION)

def get_postal(data: dict[str, Json]) -> str:
  return _get_field_value(data, _IpInfoJsonField.POSTAL)

def get_timezone(data: dict[str, Json]) -> str:
  return _get_field_value(data, _IpInfoJsonField.TIMEZONE)