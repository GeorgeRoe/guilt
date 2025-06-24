import httpx
import asyncio

class IpInfoResult:
  def __init__(self, ip, hostname, city, region, country, loc, org, postal, timezone, readme):
    self.ip = ip
    self.hostname = hostname
    self.city = city
    self.region = region
    self.country = country
    self.loc = loc
    self.org = org
    self.postal = postal
    self.timezone = timezone
    self.readme = readme
    
  @property
  def latitude(self):
    return float(self.loc.split(',')[0]) if self.loc else None

  @property
  def longitude(self):
    return float(self.loc.split(',')[1]) if self.loc else None
  
  @classmethod
  def fromDict(cls, data):
    return cls(
      data.get("ip"),
      data.get("hostname"),
      data.get("city"),
      data.get("region"),
      data.get("country"),
      data.get("loc"),
      data.get("org"),
      data.get("postal"),
      data.get("timezone"),
      data.get("readme")
    )

class IpInfoService:
  @classmethod
  def fetchData(cls):
    return IpInfoResult.fromDict(asyncio.run(cls.request()))

  @classmethod
  async def request(cls):
    async with httpx.AsyncClient() as client:
      response = await client.get("http://ipinfo.io")

      if response.status_code == 200:
        return response.json()
      else:
        raise Exception(f"Error {response.status_code}: {response.text}")