from guilt.mappers.json import MapToJson
from guilt.models.cpu_profiles_config import CpuProfilesConfig
from guilt.models.cpu_profile import CpuProfile
from guilt.models.processed_jobs_data import ProcessedJobsData
from guilt.models.processed_job import ProcessedJob
from guilt.models.unprocessed_jobs_data import UnprocessedJobsData
from guilt.models.unprocessed_job import UnprocessedJob
from datetime import datetime

def test_from_cpu_profile() -> None:
  cpu_profile = CpuProfile(name="TestProfile", tdp=95, cores=8)
  result = MapToJson.from_cpu_profile(cpu_profile)

  assert result == {
    "name": "TestProfile",
    "tdp": 95,
    "cores": 8
  }

def test_from_cpu_profiles_config() -> None:
  cpu_profile1 = CpuProfile(name="Profile1", tdp=65, cores=4)
  cpu_profile2 = CpuProfile(name="Profile2", tdp=85, cores=6)
  config = CpuProfilesConfig(default=cpu_profile1, profiles={"Profile1": cpu_profile1, "Profile2": cpu_profile2})
  
  result = MapToJson.from_cpu_profiles_config(config)

  assert result == {
    "default": "Profile1",
    "profiles": {
      "Profile1": {"tdp": 65, "cores": 4},
      "Profile2": {"tdp": 85, "cores": 6}
    }
  }

def test_from_processed_jobs_data() -> None:
  processed_jobs_data = ProcessedJobsData({
    "job1": ProcessedJob(
      start=datetime(2025, 7, 14, 12, 0),
      end=datetime(2025, 7, 15, 12, 0),
      job_id="1",
      cpu_profile=CpuProfile(name="TestProfile", tdp=95, cores=8),
      energy=100.0,
      emissions=50.0,
      generation_mix={"coal": 50, "solar": 50}
    )
  })
  
  result = MapToJson.from_processed_jobs_data(processed_jobs_data)

  assert isinstance(result, dict)
  assert result == {
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
  
def test_from_unprocessed_jobs_data() -> None:
  unprocessed_jobs_data = UnprocessedJobsData({
    "1": UnprocessedJob(job_id="1", cpu_profile=CpuProfile(name="TestProfile", tdp=95, cores=8))
  })

  result = MapToJson.from_unprocessed_jobs_data(unprocessed_jobs_data)
  
  assert isinstance(result, dict)
  assert result == {
    "1": {
      "cpu_profile": {
        "name": "TestProfile",
        "tdp": 95,
        "cores": 8
      }
    }
  }