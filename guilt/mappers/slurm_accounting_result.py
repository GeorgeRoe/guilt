from guilt.services.slurm_accounting import SlurmAccountingResult
from guilt.data.unprocessed_jobs import UnprocessedJob
from guilt.config.cpu_profiles import CpuProfile

class FromSlurmAccountingResult:
  @classmethod
  def to_unprocessed_job(cls, result: SlurmAccountingResult, cpu_profile: CpuProfile) -> UnprocessedJob:
    return UnprocessedJob(
      result.job_id,
      cpu_profile
    )