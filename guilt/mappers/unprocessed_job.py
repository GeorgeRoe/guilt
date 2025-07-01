from guilt.services.slurm_accounting import SlurmAccountingResult
from guilt.data.unprocessed_jobs import UnprocessedJob
from guilt.config.cpu_profiles import CpuProfile
    
class MapToUnprocessedJob:
  @staticmethod
  def from_slurm_accounting_result(
    slurm_accounting_result: SlurmAccountingResult,
    cpu_profile: CpuProfile
  ) -> UnprocessedJob:
    return UnprocessedJob(
      slurm_accounting_result.job_id,
      cpu_profile
    )