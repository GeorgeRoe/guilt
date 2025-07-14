import pytest
from guilt.types.json import Json
from guilt.mappers.ip_info_result import MapToIpInfoResult
from guilt.models.ip_info_result import IpInfoResult
from tests.helpers.json_helpers import all_variants_with_one_key_removed, all_variants_with_one_key_incorrectly_typed

VALID_JSON: dict[str, Json] = {
  "ip": "ip",
  "hostname": "hostname",
  "city": "city",
  "region": "region",
  "country": "country",
  "loc": "53.34411, -2.64097",
  "org": "organisation",
  "postal": "postal",
  "timezone": "timezone"
}

def test_from_json_success() -> None:
  result = MapToIpInfoResult.from_json(VALID_JSON)

  assert isinstance(result, IpInfoResult)

  assert result.ip == "ip"
  assert result.hostname == "hostname"
  assert result.city == "city"
  assert result.region == "region"
  assert result.country == "country"
  assert result.latitude == 53.34411
  assert result.longitude == -2.64097
  assert result.organisation == "organisation"
  assert result.postal == "postal"
  assert result.timezone == "timezone"

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
		MapToIpInfoResult.from_json(data)

def test_from_json_invalid_loc_raises() -> None:
  data: dict[str, Json] = {
  	**VALID_JSON,
  	"loc": "invalid,loc"
  }

  with pytest.raises(ValueError):
    MapToIpInfoResult.from_json(data)