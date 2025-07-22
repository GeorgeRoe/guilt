import pytest
from guilt.mappers.carbon_intensity_forecast_result import MapToCarbonIntensityForecastResult
from guilt.types.json import Json
from guilt.models.carbon_intensity_forecast_result import CarbonIntensityForecastResult
from guilt.models.carbon_intensity_time_segment import CarbonIntensityTimeSegment
from tests.helpers.json_helpers import all_variants_with_one_key_removed, all_variants_with_one_key_incorrectly_typed

VALID_JSON: dict[str, Json] = {
  "regionid": 13,
  "shortname": "London",
  "postcode": "SW1A",
  "data": [
    {
      "from": "2025-01-01T09:30Z",
      "to": "2025-01-01T10:00Z",
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

def _wrap(data: Json) -> dict[str, Json]:
  return {
    "data": data
  }

def test_from_json_success() -> None: 
  result = MapToCarbonIntensityForecastResult.from_json(_wrap(VALID_JSON))
  
  assert isinstance(result, CarbonIntensityForecastResult)
  assert result.region_id == 13
  assert result.short_name == "London"
  assert result.postcode == "SW1A"
  assert len(result.segments) == 1
  assert isinstance(result.segments[0], CarbonIntensityTimeSegment)

@pytest.mark.parametrize(
  "data",
  [
    (_wrap(item))
    for item
    in all_variants_with_one_key_removed(VALID_JSON) + all_variants_with_one_key_incorrectly_typed(VALID_JSON)
  ]
)
def test_from_json_invalid_raises(data: dict[str, Json]) -> None:
  with pytest.raises(ValueError):
    MapToCarbonIntensityForecastResult.from_json(data)