from guilt.repositories.registry import RepositoryRegistry
from guilt.repositories.carbon_intensity_forecast import CarbonIntensityForecastRepository
from guilt.repositories.cpu_profiles_config import CpuProfilesConfigRepository
from guilt.repositories.get_entries_password import GetEntriesPasswordRepository
from guilt.repositories.ip_info import IpInfoRepository
from guilt.repositories.processed_jobs_data import ProcessedJobsDataRepository
from guilt.repositories.slurm_accounting import SlurmAccountingRepository
from guilt.repositories.unprocessed_jobs_data import UnprocessedJobsDataRepository
from dataclasses import dataclass

@dataclass
class DependencyManager:
  repository: RepositoryRegistry
  
dependency_manager = DependencyManager(
  RepositoryRegistry(
    CarbonIntensityForecastRepository(),
    CpuProfilesConfigRepository(),
    GetEntriesPasswordRepository(),
    IpInfoRepository(),
    ProcessedJobsDataRepository(),
    SlurmAccountingRepository(),
    UnprocessedJobsDataRepository()
  )
)