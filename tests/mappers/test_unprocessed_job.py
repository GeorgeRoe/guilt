
from guilt.mappers.unprocessed_job import MapToUnprocessedJob
from guilt.models.unprocessed_job import UnprocessedJob
from guilt.models.slurm_accounting_result import SlurmAccountingResult
from guilt.models.cpu_profile import CpuProfile
from datetime import datetime

def test_from_json_success():
  slurm_accounting_result = SlurmAccountingResult(
    job_id="1",
    start_time=datetime(2025, 1, 1),
    end_time=datetime(2025, 1, 2),
    resources={
      "cpu": 8,
      "mem": 16000
    }
  )
  
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