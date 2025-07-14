import pytest
from guilt.mappers.cpu_profiles_config import MapToCpuProfilesConfig
from guilt.types.json import Json
from guilt.models.cpu_profiles_config import CpuProfilesConfig
from guilt.models.cpu_profile import CpuProfile
from tests.helpers.json_helpers import all_variants_with_one_key_removed, all_variants_with_one_key_incorrectly_typed
from typing import cast

VALID_JSON: dict[str, Json] = {
  "default": "AMD EPYC 9654",
  "profiles": {
    "AMD EPYC 9654": {
      "tdp": 360,
      "cores": 96
    }
  }
}

def test_from_json_sucess() -> None:
  result = MapToCpuProfilesConfig.from_json(VALID_JSON)

  assert isinstance(result, CpuProfilesConfig)
	
  assert result.default.name == "AMD EPYC 9654"
  assert result.default.tdp == 360
  assert result.default.cores == 96

  assert len(result.profiles) == 1
  assert isinstance(result.profiles.get("AMD EPYC 9654"), CpuProfile)
  assert result.profiles.get("AMD EPYC 9654") != None

  assert cast(CpuProfile, result.profiles.get("AMD EPYC 9654")).name == "AMD EPYC 9654"
  assert cast(CpuProfile, result.profiles.get("AMD EPYC 9654")).tdp == 360
  assert cast(CpuProfile, result.profiles.get("AMD EPYC 9654")).cores == 96

@pytest.mark.parametrize(
	"data",
	[
		(item)
		for item
		in all_variants_with_one_key_removed(VALID_JSON) + all_variants_with_one_key_incorrectly_typed(VALID_JSON, {"tdp"})
	]
)
def test_from_json_invalid_raises(data: dict[str, Json]) -> None:
	with pytest.raises(ValueError):
		MapToCpuProfilesConfig.from_json(data)
		
def test_from_json_invalid_default_profile_raises() -> None:
  data: dict[str, Json] = {
	  **VALID_JSON,
	  "default": "Nonexistent CPU"
  }
	
  with pytest.raises(ValueError):
    MapToCpuProfilesConfig.from_json(data)