import pytest
from guilt.mappers.carbon_intensity_time_segment import MapToCarbonIntensityTimeSegment
from guilt.types.json import Json
from guilt.models.carbon_intensity_time_segment import CarbonIntensityTimeSegment
from tests.helpers.json_helpers import all_variants_with_one_key_removed, all_variants_with_one_key_incorrectly_typed
from datetime import datetime, timezone

VALID_JSON: dict[str, Json] = {
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

def test_from_json_success() -> None: 
  result = MapToCarbonIntensityTimeSegment.from_json(VALID_JSON)
  
  assert isinstance(result, CarbonIntensityTimeSegment)
  assert result.from_time == datetime(2025, 1, 1, 9, 30, tzinfo=timezone.utc)
  assert result.to_time == datetime(2025, 1, 1, 10, 0, tzinfo=timezone.utc)
  assert result.intensity == 40
  assert result.index == "low"
  assert result.generation_mix == {
    "biomass": 0.9,
    "coal": 0,
    "imports": 10.6,
    "gas": 6.8,
    "nuclear": 16.1,
    "other": 0,
    "hydro": 0.2,
    "solar": 0.5,
    "wind": 64.9
  }

@pytest.mark.parametrize(
  "data",
  [
    (item)
    for item
    in all_variants_with_one_key_removed(VALID_JSON) + all_variants_with_one_key_incorrectly_typed(VALID_JSON)
  ]
)
def test_from_json_invalid_raises(data: dict[str, Json]) -> None:
  with pytest.raises(ValueError):
    MapToCarbonIntensityTimeSegment.from_json(data)