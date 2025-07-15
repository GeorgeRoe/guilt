import pytest
from guilt.mappers.unprocessed_jobs_data import MapToUnprocessedJobsData
from guilt.types.json import Json
from guilt.models.unprocessed_jobs_data import UnprocessedJobsData
from guilt.models.unprocessed_job import UnprocessedJob

VALID_JSON: dict[str, Json] = {
  "job1": {
    "cpu_profile": {
      "name": "TestProfile",
      "tdp": 95,
      "cores": 8
    }
  }
}

def test_from_json_sucess() -> None:
  result = MapToUnprocessedJobsData.from_json(VALID_JSON)

  assert isinstance(result, UnprocessedJobsData)
  assert len(result.jobs) == 1
  assert isinstance(result.jobs.get("job1"), UnprocessedJob)
  assert result.jobs.get("job1") != None

def test_from_json_empty_sucess() -> None:
  result = MapToUnprocessedJobsData.from_json({})
  
  assert isinstance(result, UnprocessedJobsData)
  assert len(result.jobs) == 0

def test_from_json_invalid_raises() -> None:
  with pytest.raises(ValueError):
    MapToUnprocessedJobsData.from_json({ "job1": "not a job" })
    MapToUnprocessedJobsData.from_json({ "job1": None })