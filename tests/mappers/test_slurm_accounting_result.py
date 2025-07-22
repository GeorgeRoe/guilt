import pytest
from guilt.mappers.slurm_accounting_result import MapToSlurmAccountingResult
from guilt.types.json import Json
from guilt.models.slurm_accounting_result import SlurmAccountingResult
from tests.helpers.json_helpers import all_variants_with_one_key_removed, all_variants_with_one_key_incorrectly_typed
from datetime import datetime, timezone

VALID_JSON: dict[str, Json] = {
  "job_id": "1",
  "time": {
    "start": 1752534000,
    "end": 1752620400
  },
  "tres": {
    "allocated": [
      {
        "type": "cpu",
        "count": 8
      },
      {
        "type": "mem",
        "count": 16000
      }
    ]
  }
}

def test_from_json_success():
  result = MapToSlurmAccountingResult.from_json(VALID_JSON)
  
  assert isinstance(result, SlurmAccountingResult)
  
  assert result.job_id == "1"
  assert result.start_time == datetime(2025, 7, 15, tzinfo=timezone.utc)
  assert result.end_time == datetime(2025, 7, 16, tzinfo=timezone.utc)
  assert result.resources == {
    "cpu": 8,
    "mem": 16000
  }
  
@pytest.mark.parametrize(
	"data",
	[
		(item)
		for item
		in all_variants_with_one_key_removed(VALID_JSON) + all_variants_with_one_key_incorrectly_typed(VALID_JSON, {"tdp"}, {"job_id"})
	]
)
def test_from_json_invalid_raises(data: dict[str, Json]) -> None:
	with pytest.raises(ValueError):
		MapToSlurmAccountingResult.from_json(data)