from guilt.repositories.cpu_profiles_config import CpuProfilesConfigRepository
from guilt.models.slurm_accounting_result import SlurmAccountingResult
from guilt.models.unprocessed_job import UnprocessedJob
from guilt.mappers.unprocessed_job import MapToUnprocessedJob

class BackfillService:
  def __init__(
    self,
    cpu_profiles_config_repository: CpuProfilesConfigRepository
  ):
    self.cpu_profiles_config_repository = cpu_profiles_config_repository
    
  def convert_slurm_jobs_to_unprocessed_jobs(self, slurm_accounting_results: list[SlurmAccountingResult]) -> list[UnprocessedJob]:
    default_cpu_profile = self.cpu_profiles_config_repository.fetch_data().default
    
    return [MapToUnprocessedJob.from_slurm_accounting_result(result, default_cpu_profile) for result in slurm_accounting_results]
    
  