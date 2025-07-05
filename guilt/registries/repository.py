from guilt.repositories.carbon_intensity_forecast import CarbonIntensityForecastRepository
from guilt.repositories.cpu_profiles_config import CpuProfilesConfigRepository
from guilt.repositories.environment_variables import EnvironmentVariablesRepository
from guilt.repositories.get_entries_password import GetEntriesPasswordRepository
from guilt.repositories.ip_info import IpInfoRepository
from guilt.repositories.processed_jobs_data import ProcessedJobsDataRepository
from guilt.repositories.slurm_accounting import SlurmAccountingRepository
from guilt.repositories.unprocessed_jobs_data import UnprocessedJobsDataRepository
from dataclasses import dataclass

@dataclass
class RepositoryRegistry:
  carbon_intensity_forecast: CarbonIntensityForecastRepository = CarbonIntensityForecastRepository()
  cpu_profiles_config: CpuProfilesConfigRepository = CpuProfilesConfigRepository()
  environment_varialbes: EnvironmentVariablesRepository = EnvironmentVariablesRepository()
  get_entries_password: GetEntriesPasswordRepository = GetEntriesPasswordRepository()
  ip_info: IpInfoRepository = IpInfoRepository()
  processed_jobs_data: ProcessedJobsDataRepository = ProcessedJobsDataRepository()
  slurm_accounting: SlurmAccountingRepository = SlurmAccountingRepository()
  unprocessed_jobs_data: UnprocessedJobsDataRepository = UnprocessedJobsDataRepository()