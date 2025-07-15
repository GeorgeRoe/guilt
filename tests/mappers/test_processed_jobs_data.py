import pytest
from guilt.mappers.processed_jobs_data import MapToProcessedJobsData
from guilt.types.json import Json
from guilt.models.processed_jobs_data import ProcessedJobsData
from guilt.models.processed_job import ProcessedJob

VALID_JSON: dict[str, Json] = {
  "job1": {
    "start": "2025-07-14T12:00:00",
    "end": "2025-07-15T12:00:00",
    "cpu_profile": {
      "name": "TestProfile",
      "tdp": 95,
      "cores": 8
    },
    "energy": 100.0,
    "emissions": 50.0,
    "generation_mix": {"coal": 50, "solar": 50}
  }
}

def test_from_json_sucess() -> None:
  result = MapToProcessedJobsData.from_json(VALID_JSON)

  assert isinstance(result, ProcessedJobsData)
  assert len(result.jobs) == 1
  assert isinstance(result.jobs.get("job1"), ProcessedJob)
  assert result.jobs.get("job1") != None

def test_from_json_empty_sucess() -> None:
  result = MapToProcessedJobsData.from_json({})
  
  assert isinstance(result, ProcessedJobsData)
  assert len(result.jobs) == 0

def test_from_json_invalid_raises() -> None:
  with pytest.raises(ValueError):
    MapToProcessedJobsData.from_json({ "job1": "not a job" })
    MapToProcessedJobsData.from_json({ "job1": None })