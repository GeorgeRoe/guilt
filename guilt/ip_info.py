import httpx
import asyncio

class IpInfo:
  def __init__(self):
    data = asyncio.run(self.request())

    self.ip = data.get("ip")
    self.hostname = data.get("hostname")
    self.city = data.get("city")
    self.region = data.get("region")
    self.country = data.get("country")
    self.loc = data.get("loc")
    self.org = data.get("org")
    self.postal = data.get("postal")
    self.timezone = data.get("timezone")
    self.readme = data.get("readme")

  @property
  def latitude(self):
    return float(self.loc.split(',')[0]) if self.loc else None

  @property
  def longitude(self):
    return float(self.loc.split(',')[1]) if self.loc else None

  def __repr__(self):
    return (f"IpInfo(ip={self.ip}, city={self.city}, region={self.region}, "
            f"country={self.country}, org={self.org})")
  
  @classmethod
  async def request(cls):
    async with httpx.AsyncClient() as client:
      response = await client.get("http://ipinfo.io")

      if response.status_code == 200:
        return response.json()
      else:
        raise Exception(f"Error {response.status_code}: {response.text}")
