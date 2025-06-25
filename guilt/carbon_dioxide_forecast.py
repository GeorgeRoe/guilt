import asyncio
import httpx
from guilt.log import logger
from typing import Dict

class Intensity:
  def __init__(self, forecast: int, index: str):
    self.forecast = forecast
    self.index = index

  def __repr__(self):
    return f"Intensity(forecast={self.forecast}, index={self.index!r})"

class DataEntry:
  def __init__(self, from_time: str, to_time: str, intensity: Intensity, generationmix: Dict[str, float]):
    self.from_time = from_time
    self.to_time = to_time
    self.intensity = intensity
    self.generationmix = generationmix

  def __repr__(self):
    return (f"DataEntry(from={self.from_time}, to={self.to_time}, "
            f"intensity={self.intensity}, generationmix={self.generationmix})")

class CarbonDioxideForecast:
  def __init__(self, from_dt, to_dt, postcode):
    logger.info(f"Fetching carbon forecast from {from_dt} to {to_dt} for postcode {postcode}")
    try:
      data = asyncio.run(self.request(from_dt, to_dt, postcode))['data']
    except Exception as e:
      logger.error(f"Failed to fetch carbon forecast: {e}")
      raise

    self.regionid = data.get("regionid")
    self.shortname = data.get("shortname")
    self.postcode = data.get("postcode")
    self.entries = []

    logger.debug(f"Parsing {len(data.get('data', []))} forecast entries")
    for entry in data.get("data", []):
      intensity_data = entry.get("intensity", {})
      intensity = Intensity(intensity_data.get("forecast"), intensity_data.get("index"))
      generationmix = {fuel["fuel"]: fuel["perc"] for fuel in entry.get("generationmix", [])}

      data_entry = DataEntry(entry.get("from"), entry.get("to"), intensity, generationmix)
      logger.debug(f"Parsed entry: {data_entry}")
      self.entries.append(data_entry)

    self.entries = sorted(self.entries, key=lambda x: x.from_time)
    logger.info(f"Carbon forecast loaded: {len(self.entries)} entries sorted by start time")

  def __repr__(self):
    return (f"CarbonDioxideForecast(regionid={self.regionid}, shortname={self.shortname}, "
            f"postcode={self.postcode}, entries={len(self.entries)} entries)")

  @classmethod
  async def request(cls, from_dt, to_dt, postcode):
    from_str = from_dt.strftime('%Y-%m-%dT%H:%MZ')
    to_str = to_dt.strftime('%Y-%m-%dT%H:%MZ')
    url = f"https://api.carbonintensity.org.uk/regional/intensity/{from_str}/{to_str}/postcode/{postcode}"

    logger.debug(f"Sending request to: {url}")
    async with httpx.AsyncClient() as client:
      response = await client.get(url)

    if response.status_code == 200:
      logger.debug("Received successful response from carbon intensity API")
      return response.json()
    else:
      logger.error(f"API request failed: {response.status_code} {response.text}")
      raise Exception(f"Error {response.status_code}: {response.text}")