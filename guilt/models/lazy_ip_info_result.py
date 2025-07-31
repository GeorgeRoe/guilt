from typing import Optional
from guilt.parsers import parse_ip_info_json
from guilt.types.json import Json
from guilt.models.location import Location

class LazyIpInfoResult:
  def __init__(self, data: dict[str, Json]) -> None:
    self._data = data

    self._ip: Optional[str] = None
    self._hostname: Optional[str] = None
    self._city: Optional[str] = None
    self._region: Optional[str] = None
    self._country: Optional[str] = None
    self._location: Optional[Location] = None
    self._organisation: Optional[str] = None
    self._postal: Optional[str] = None
    self._timezone: Optional[str] = None

  @property
  def ip(self) -> str:
    if self._ip is None:
      self._ip = parse_ip_info_json.get_ip(self._data)
    return self._ip
  
  @property
  def hostname(self) -> Optional[str]:
    if self._hostname is None:
      self._hostname = parse_ip_info_json.get_hostname(self._data)
    return self._hostname
  
  @property
  def city(self) -> str:
    if self._city is None:
      self._city = parse_ip_info_json.get_city(self._data)
    return self._city
  
  @property
  def region(self) -> str:
    if self._region is None:
      self._region = parse_ip_info_json.get_region(self._data)
    return self._region
  
  @property
  def country(self) -> str:
    if self._country is None:
      self._country = parse_ip_info_json.get_country(self._data)
    return self._country
  
  @property
  def location(self) -> Location:
    if self._location is None:
      self._location = parse_ip_info_json.get_location(self._data)
    return self._location

  @property
  def organisation(self) -> Optional[str]:
    if self._organisation is None:
      self._organisation = parse_ip_info_json.get_organisation(self._data)
    return self._organisation

  @property
  def postal(self) -> Optional[str]:
    if self._postal is None:
      self._postal = parse_ip_info_json.get_postal(self._data)
    return self._postal
  
  @property
  def timezone(self) -> Optional[str]:
    if self._timezone is None:
      self._timezone = parse_ip_info_json.get_timezone(self._data)
    return self._timezone