from guilt.interfaces.services.backfill import BackfillServiceInterface
from guilt.interfaces.services.cpu_profiles_config import CpuProfilesConfigServiceInterface
from guilt.models.lazy_slurm_accounting_result import LazySlurmAccountingResult
from guilt.models.unprocessed_job import UnprocessedJob
from guilt.mappers import map_to

class BackfillService(BackfillServiceInterface):
  def __init__(
    self,
    cpu_profiles_config_service: CpuProfilesConfigServiceInterface
  ):
    self.cpu_profiles_config_service = cpu_profiles_config_service
  
  def convert_slurm_jobs_to_unprocessed_jobs(self, slurm_accounting_results: list[LazySlurmAccountingResult]) -> list[UnprocessedJob]:
    default_cpu_profile = self.cpu_profiles_config_service.read_from_file().default
    
    return [map_to.unprocessed_job.from_slurm_accounting_result(result, default_cpu_profile) for result in slurm_accounting_results]
    
  