from guilt.registries.repository import RepositoryRegistry
from guilt.repositories.carbon_intensity_forecast import CarbonIntensityForecastRepository
from guilt.repositories.cpu_profiles_config import CpuProfilesConfigRepository
from guilt.repositories.get_entries_password import GetEntriesPasswordRepository
from guilt.repositories.ip_info import IpInfoRepository
from guilt.repositories.processed_jobs_data import ProcessedJobsDataRepository
from guilt.repositories.slurm_accounting import SlurmAccountingRepository
from guilt.repositories.unprocessed_jobs_data import UnprocessedJobsDataRepository
from guilt.registries.service import ServiceRegistry
from guilt.services.setup import SetupService
from dataclasses import dataclass

@dataclass
class DependencyManager:
  repository: RepositoryRegistry
  service: ServiceRegistry
  
def construct_default_dependency_manager() -> DependencyManager:
  repositories = RepositoryRegistry(
    CarbonIntensityForecastRepository(),
    CpuProfilesConfigRepository(),
    GetEntriesPasswordRepository(),
    IpInfoRepository(),
    ProcessedJobsDataRepository(),
    SlurmAccountingRepository(),
    UnprocessedJobsDataRepository()
  )
  
  services = ServiceRegistry(
    SetupService(
      repositories.cpu_profiles_config,
      repositories.processed_jobs_data,
      repositories.unprocessed_jobs_data
    )
  )
  
  return DependencyManager(repositories, services)

dependency_manager = construct_default_dependency_manager()