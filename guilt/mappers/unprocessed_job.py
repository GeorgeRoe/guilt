from guilt.models.lazy_slurm_accounting_result import LazySlurmAccountingResult
from guilt.models.unprocessed_job import UnprocessedJob
from guilt.models.cpu_profile import CpuProfile
    
class MapToUnprocessedJob:
  @staticmethod
  def from_slurm_accounting_result(
    slurm_accounting_result: LazySlurmAccountingResult,
    cpu_profile: CpuProfile
  ) -> UnprocessedJob:
    return UnprocessedJob(
      slurm_accounting_result.job_id,
      cpu_profile
    )