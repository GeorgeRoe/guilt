from guilt.interfaces.services.setup import SetupServiceInterface
from guilt.interfaces.services.cpu_profiles_config import CpuProfilesConfigServiceInterface
from guilt.interfaces.services.processed_jobs_data import ProcessedJobsDataServiceInterface
from guilt.interfaces.services.unprocessed_jobs_data import UnprocessedJobsDataServiceInterface
from guilt.services.setup import SetupService
from tests.mocks.services.cpu_profiles_config import MockCpuProfilesConfigService
from tests.mocks.services.processed_jobs_data import MockProcessedJobsDataService
from tests.mocks.services.unprocessed_jobs_data import MockUnprocessedJobsDataService
from guilt.dependencies.injector import DependencyInjector
from guilt.models.cpu_profile import CpuProfile
from guilt.models.cpu_profiles_config import CpuProfilesConfig
from guilt.models.processed_jobs_data import ProcessedJobsData
from guilt.models.unprocessed_jobs_data import UnprocessedJobsData

default_profile = CpuProfile("AMD EPYC 9654", 360, 96)
    
profiles = [
  default_profile,
  CpuProfile("AMD EPYC 7502", 180, 32),
  CpuProfile("AMD EPYC 7742", 225, 64),
  CpuProfile("AMD EPYC 7543P", 225, 32)
]
  
DEFAULT_CPU_PROFILES_CONFIG = CpuProfilesConfig(default_profile, {profile.name: profile for profile in profiles})

def test_setup_cpu_profiles_config_file_success() -> None:
  cpu_profiles_service = MockCpuProfilesConfigService(DEFAULT_CPU_PROFILES_CONFIG)
  
  di = DependencyInjector()
  di.register_instance(CpuProfilesConfigServiceInterface, cpu_profiles_service)
  di.register_instance(ProcessedJobsDataServiceInterface, MockProcessedJobsDataService())
  di.register_instance(UnprocessedJobsDataServiceInterface, MockUnprocessedJobsDataService())
  di.bind(SetupServiceInterface, SetupService)
  setup_service = di.resolve(SetupServiceInterface) # type: ignore[type-abstract]
  
  result = setup_service.setup_cpu_profiles_config_file()
  
  assert result
  assert cpu_profiles_service.read_from_file() == cpu_profiles_service.get_default()
  
def test_setup_cpu_profiles_config_file_failure() -> None:
  di = DependencyInjector()
  di.register_instance(CpuProfilesConfigServiceInterface, MockCpuProfilesConfigService(DEFAULT_CPU_PROFILES_CONFIG, True))
  di.register_instance(ProcessedJobsDataServiceInterface, MockProcessedJobsDataService())
  di.register_instance(UnprocessedJobsDataServiceInterface, MockUnprocessedJobsDataService())
  di.bind(SetupServiceInterface, SetupService)
  setup_service = di.resolve(SetupServiceInterface) # type: ignore[type-abstract]
  
  result = setup_service.setup_cpu_profiles_config_file()
  
  assert not result

def test_setup_processed_jobs_data_file_success() -> None:
  processed_jobs_data_service = MockProcessedJobsDataService()
  
  di = DependencyInjector()
  di.register_instance(CpuProfilesConfigServiceInterface, MockCpuProfilesConfigService(DEFAULT_CPU_PROFILES_CONFIG))
  di.register_instance(ProcessedJobsDataServiceInterface, processed_jobs_data_service)
  di.register_instance(UnprocessedJobsDataServiceInterface, MockUnprocessedJobsDataService())
  di.bind(SetupServiceInterface, SetupService)
  setup_service = di.resolve(SetupServiceInterface) # type: ignore[type-abstract]
  
  result = setup_service.setup_processed_jobs_data_file()
  
  assert result
  assert processed_jobs_data_service.read_from_file() == ProcessedJobsData({})
  
def test_setup_processed_jobs_data_file_failure() -> None:
  processed_jobs_data_service = MockProcessedJobsDataService(fail=True)
  
  di = DependencyInjector()
  di.register_instance(CpuProfilesConfigServiceInterface, MockCpuProfilesConfigService(DEFAULT_CPU_PROFILES_CONFIG))
  di.register_instance(ProcessedJobsDataServiceInterface, processed_jobs_data_service)
  di.register_instance(UnprocessedJobsDataServiceInterface, MockUnprocessedJobsDataService())
  di.bind(SetupServiceInterface, SetupService)
  setup_service = di.resolve(SetupServiceInterface) # type: ignore[type-abstract]
  
  result = setup_service.setup_processed_jobs_data_file()
  
  assert not result
  
def test_setup_unprocessed_jobs_data_file_success() -> None:
  unprocessed_jobs_data_service = MockUnprocessedJobsDataService()
  
  di = DependencyInjector()
  di.register_instance(CpuProfilesConfigServiceInterface, MockCpuProfilesConfigService(DEFAULT_CPU_PROFILES_CONFIG))
  di.register_instance(ProcessedJobsDataServiceInterface, MockProcessedJobsDataService())
  di.register_instance(UnprocessedJobsDataServiceInterface, unprocessed_jobs_data_service)
  di.bind(SetupServiceInterface, SetupService)
  setup_service = di.resolve(SetupServiceInterface) # type: ignore[type-abstract]
  
  result = setup_service.setup_unprocessed_jobs_data_file()
  
  assert result
  assert unprocessed_jobs_data_service.read_from_file() == UnprocessedJobsData({})
  
def test_setup_unprocessed_jobs_data_file_failure() -> None:
  unprocessed_jobs_data_service = MockUnprocessedJobsDataService(fail=True)
  
  di = DependencyInjector()
  di.register_instance(CpuProfilesConfigServiceInterface, MockCpuProfilesConfigService(DEFAULT_CPU_PROFILES_CONFIG))
  di.register_instance(ProcessedJobsDataServiceInterface, MockProcessedJobsDataService())
  di.register_instance(UnprocessedJobsDataServiceInterface, unprocessed_jobs_data_service)
  di.bind(SetupServiceInterface, SetupService)
  setup_service = di.resolve(SetupServiceInterface) # type: ignore[type-abstract]
  
  result = setup_service.setup_unprocessed_jobs_data_file()
  
  assert not result
  
def test_setup_all_files_success() -> None:
  di = DependencyInjector()
  di.register_instance(CpuProfilesConfigServiceInterface, MockCpuProfilesConfigService(DEFAULT_CPU_PROFILES_CONFIG))
  di.register_instance(ProcessedJobsDataServiceInterface, MockProcessedJobsDataService())
  di.register_instance(UnprocessedJobsDataServiceInterface, MockUnprocessedJobsDataService())
  di.bind(SetupServiceInterface, SetupService)
  setup_service = di.resolve(SetupServiceInterface) # type: ignore[type-abstract]
  
  result = setup_service.setup_all_files()
  
  assert result
  
def test_setup_all_files_failure_cpu_profiles_config() -> None:
  di = DependencyInjector()
  di.register_instance(CpuProfilesConfigServiceInterface, MockCpuProfilesConfigService(DEFAULT_CPU_PROFILES_CONFIG, fail=True))
  di.register_instance(ProcessedJobsDataServiceInterface, MockProcessedJobsDataService())
  di.register_instance(UnprocessedJobsDataServiceInterface, MockUnprocessedJobsDataService())
  di.bind(SetupServiceInterface, SetupService)
  setup_service = di.resolve(SetupServiceInterface) # type: ignore[type-abstract]
  
  result = setup_service.setup_all_files()
  
  assert not result
  
def test_setup_all_files_failure_processed_jobs_data() -> None:
  di = DependencyInjector()
  di.register_instance(CpuProfilesConfigServiceInterface, MockCpuProfilesConfigService(DEFAULT_CPU_PROFILES_CONFIG))
  di.register_instance(ProcessedJobsDataServiceInterface, MockProcessedJobsDataService(fail=True))
  di.register_instance(UnprocessedJobsDataServiceInterface, MockUnprocessedJobsDataService())
  di.bind(SetupServiceInterface, SetupService)
  setup_service = di.resolve(SetupServiceInterface) # type: ignore[type-abstract]
  
  result = setup_service.setup_all_files()
  
  assert not result
  
def test_setup_all_files_failure_unprocessed_jobs_data() -> None:
  di = DependencyInjector()
  di.register_instance(CpuProfilesConfigServiceInterface, MockCpuProfilesConfigService(DEFAULT_CPU_PROFILES_CONFIG))
  di.register_instance(ProcessedJobsDataServiceInterface, MockProcessedJobsDataService())
  di.register_instance(UnprocessedJobsDataServiceInterface, MockUnprocessedJobsDataService(fail=True))
  di.bind(SetupServiceInterface, SetupService)
  setup_service = di.resolve(SetupServiceInterface) # type: ignore[type-abstract]
  
  result = setup_service.setup_all_files()
  
  assert not result