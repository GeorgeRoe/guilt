class IpInfoResult:
  def __init__(
    self,
    ip: str,
    hostname: str,
    city: str,
    region: str,
    country: str,
    latitude: float,
    longitude: float,
    organisation: str,
    postal: str,
    timezone: str
  ):
    self.ip = ip
    self.hostname = hostname
    self.city = city
    self.region = region
    self.country = country
    self.latitude = latitude
    self.longitude = longitude
    self.organisation = organisation
    self.postal = postal
    self.timezone = timezone