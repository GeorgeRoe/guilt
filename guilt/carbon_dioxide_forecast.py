import asyncio
import httpx

class Intensity:
  def __init__(self, forecast: int, index: str):
    self.forecast = forecast
    self.index = index

  def __repr__(self):
    return f"Intensity(forecast={self.forecast}, index={self.index!r})"

class DataEntry:
  def __init__(self, from_time: str, to_time: str, intensity: Intensity, generationmix: dict):
    self.from_time = from_time
    self.to_time = to_time
    self.intensity = intensity
    self.generationmix = generationmix

  def __repr__(self):
    return (f"DataEntry(from={self.from_time}, to={self.to_time}, "
            f"intensity={self.intensity}, generationmix={self.generationmix})")

class CarbonDioxideForecast:
  def __init__(self, from_dt, to_dt, postcode):
    data = asyncio.run(self.request(from_dt, to_dt, postcode))['data']

    self.regionid = data.get("regionid")
    self.shortname = data.get("shortname")
    self.postcode = data.get("postcode")
    self.entries = []

    for entry in data.get("data", []):
      intensity_data = entry.get("intensity", {})
      intensity = Intensity(intensity_data.get("forecast"), intensity_data.get("index"))

      generationmix = {fuel["fuel"]: fuel["perc"] for fuel in entry.get("generationmix", [])}

      self.entries.append(DataEntry(
        entry.get("from"),
        entry.get("to"),
        intensity,
        generationmix
      ))

    self.entries = sorted(self.entries, key=lambda x: x.from_time)

  def __repr__(self):
    return (f"CarbonDioxideForecast(regionid={self.regionid}, shortname={self.shortname}, "
            f"postcode={self.postcode}, entries={len(self.entries)} entries)")

  @classmethod
  async def request(cls, from_dt, to_dt, postcode):
    from_str = from_dt.strftime('%Y-%m-%dT%H:%MZ')
    to_str = to_dt.strftime('%Y-%m-%dT%H:%MZ')

    async with httpx.AsyncClient() as client:
      response = await client.get(
        f"https://api.carbonintensity.org.uk/regional/intensity/{from_str}/{to_str}/postcode/{postcode}"
      )

      if response.status_code == 200:
        return response.json()
      else:
        raise Exception(f"Error {response.status_code}: {response.text}")
