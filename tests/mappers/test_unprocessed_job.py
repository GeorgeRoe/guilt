
from guilt.mappers.unprocessed_job import MapToUnprocessedJob
from guilt.models.unprocessed_job import UnprocessedJob
from guilt.models.lazy_slurm_accounting_result import LazySlurmAccountingResult
from guilt.models.cpu_profile import CpuProfile
from datetime import datetime

def test_from_json_success():
  slurm_accounting_result = LazySlurmAccountingResult({
    "job_id": "1",
    "time": {
      "start": datetime(2025, 1, 1).timestamp(),
      "end": datetime(2025, 1, 2).timestamp()
    },
    "tres": {
      "allocated": [
        {"type": "cpu", "count": 8},
        {"type": "mem", "count": 16000}
      ]
    }
  })
  
  cpu_profile = CpuProfile(
    name="TestProfile",
    tdp=95,
    cores=8
  )
  
  result = MapToUnprocessedJob.from_slurm_accounting_result(
    slurm_accounting_result,
    cpu_profile
  )
  
  assert isinstance(result, UnprocessedJob)
  assert result.cpu_profile == cpu_profile
  assert result.job_id == slurm_accounting_result.job_id