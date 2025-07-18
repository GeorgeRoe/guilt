import respx
import httpx
import pytest
from guilt.interfaces.services.carbon_intensity_forecast import CarbonIntensityForecastServiceInterface
from guilt.services.carbon_intensity_forecast import CarbonIntensityForecastService
from guilt.models.carbon_intensity_forecast_result import CarbonIntensityForecastResult
from guilt.dependencies.injector import DependencyInjector
from guilt.types.json import Json
from datetime import datetime

@respx.mock
def test_get_forecast_success() -> None:
  di = DependencyInjector()
  di.bind(CarbonIntensityForecastServiceInterface, CarbonIntensityForecastService)
  carbon_intensity_forecast_service = di.resolve(CarbonIntensityForecastServiceInterface) # type: ignore[type-abstract]
  
  from_time = datetime(2025, 1, 1, 9, 30)
  to_time = datetime(2025, 1, 1, 10)
  postcode = "SW1A"
  
  time_format = "%Y-%m-%dT%H:%MZ"
  from_str = from_time.strftime(time_format)
  to_str = to_time.strftime(time_format)
  url = f"https://api.carbonintensity.org.uk/regional/intensity/{from_str}/{to_str}/postcode/{postcode}"
  
  response: dict[str, Json] = {
    "regionid": 13,
    "shortname": "London",
    "postcode": postcode,
    "data": [
      {
        "from": from_str,
        "to": to_str,
        "intensity": {
          "forecast": 40,
          "index": "low"
        },
        "generationmix": [
          {
            "fuel": "biomass",
            "perc": 0.9
          },
          {
            "fuel": "coal",
            "perc": 0
          },
          {
            "fuel": "imports",
            "perc": 10.6
          },
          {
            "fuel": "gas",
            "perc": 6.8
          },
          {
            "fuel": "nuclear",
            "perc": 16.1
          },
          {
            "fuel": "other",
            "perc": 0
          },
          {
            "fuel": "hydro",
            "perc": 0.2
          },
          {
            "fuel": "solar",
            "perc": 0.5
          },
          {
            "fuel": "wind",
            "perc": 64.9
          }
        ]
      }
    ]
  }
  
  respx.get(url).mock(return_value=httpx.Response(200, json=response))
  
  result = carbon_intensity_forecast_service.get_forecast(from_time, to_time, postcode)
  
  assert isinstance(result, CarbonIntensityForecastResult)
  
@respx.mock
def test_get_forecast_raises() -> None:
  di = DependencyInjector()
  di.bind(CarbonIntensityForecastServiceInterface, CarbonIntensityForecastService)
  carbon_intensity_forecast_service = di.resolve(CarbonIntensityForecastServiceInterface) # type: ignore[type-abstract]
  
  from_time = datetime(2025, 1, 1, 9, 30)
  to_time = datetime(2025, 1, 1, 10)
  postcode = "SW1A"
  
  time_format = "%Y-%m-%dT%H:%MZ"
  from_str = from_time.strftime(time_format)
  to_str = to_time.strftime(time_format)
  url = f"https://api.carbonintensity.org.uk/regional/intensity/{from_str}/{to_str}/postcode/{postcode}"
  
  respx.get(url).mock(return_value=httpx.Response(404))
  
  with pytest.raises(Exception):
    carbon_intensity_forecast_service.get_forecast(from_time, to_time, postcode)