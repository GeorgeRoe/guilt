from guilt.dependencies.injector import DependencyInjector
from guilt.registries.service import ServiceRegistry

from guilt.services.backfill import BackfillService
from guilt.services.carbon_intensity_forecast import CarbonIntensityForecastService
from guilt.services.cpu_profiles_config import CpuProfilesConfigService
from guilt.services.environment_variables import EnvironmentVariablesService
from guilt.services.file_system import FileSystemService
from guilt.services.get_entries_password import GetEntriesPasswordService
from guilt.services.guilt_directory import GuiltDirectoryService
from guilt.services.ip_info import IpInfoService
from guilt.services.processed_jobs_data import ProcessedJobsDataService
from guilt.services.setup import SetupService
from guilt.services.slurm_accounting import SlurmAccountingService
from guilt.services.slurm_batch import SlurmBatchService
from guilt.services.unprocessed_jobs_data import UnprocessedJobsDataService

from guilt.interfaces.services.backfill import BackfillServiceInterface
from guilt.interfaces.services.carbon_intensity_forecast import CarbonIntensityForecastServiceInterface
from guilt.interfaces.services.cpu_profiles_config import CpuProfilesConfigServiceInterface
from guilt.interfaces.services.environment_variables import EnvironmentVariablesServiceInterface
from guilt.interfaces.services.file_system import FileSystemServiceInterface
from guilt.interfaces.services.get_entries_password import GetEntriesPasswordServiceInterface
from guilt.interfaces.services.guilt_directory import GuiltDirectoryServiceInterface
from guilt.interfaces.services.ip_info import IpInfoServiceInterface
from guilt.interfaces.services.processed_jobs_data import ProcessedJobsDataServiceInterface
from guilt.interfaces.services.setup import SetupServiceInterface
from guilt.interfaces.services.slurm_accounting import SlurmAccountingServiceInterface
from guilt.interfaces.services.slurm_batch import SlurmBatchServiceInterface
from guilt.interfaces.services.unprocessed_jobs_data import UnprocessedJobsDataServiceInterface

def construct_default_service_registry() -> ServiceRegistry:
  di = DependencyInjector()
  
  di.bind(BackfillServiceInterface, BackfillService)
  di.bind(CarbonIntensityForecastServiceInterface, CarbonIntensityForecastService)
  di.bind(CpuProfilesConfigServiceInterface, CpuProfilesConfigService)
  di.bind(EnvironmentVariablesServiceInterface, EnvironmentVariablesService)
  di.bind(FileSystemServiceInterface, FileSystemService)
  di.bind(GetEntriesPasswordServiceInterface, GetEntriesPasswordService)
  di.bind(GuiltDirectoryServiceInterface, GuiltDirectoryService)
  di.bind(IpInfoServiceInterface, IpInfoService)
  di.bind(ProcessedJobsDataServiceInterface, ProcessedJobsDataService)
  di.bind(SetupServiceInterface, SetupService)
  di.bind(SlurmAccountingServiceInterface, SlurmAccountingService)
  di.bind(SlurmBatchServiceInterface, SlurmBatchService)
  di.bind(UnprocessedJobsDataServiceInterface, UnprocessedJobsDataService)
  
  return di.build(ServiceRegistry)