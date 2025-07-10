import pytest
from guilt.mappers.cpu_profile import MapToCpuProfile
from guilt.types.json import Json
from guilt.models.cpu_profile import CpuProfile
from tests.helpers.json_helpers import all_variants_with_one_key_removed, all_variants_with_one_key_incorrectly_typed

VALID_JSON: dict[str, Json] = {
	"name": "AMD EPYC 9654",
	"tdp": 360,
	"cores": 96	 
}

def test_from_json_sucess() -> None:
	result = MapToCpuProfile.from_json(VALID_JSON)

	assert isinstance(result, CpuProfile)
	assert result.name == "AMD EPYC 9654"
	assert result.tdp == 360
	assert result.cores == 96

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
    MapToCpuProfile.from_json(data)