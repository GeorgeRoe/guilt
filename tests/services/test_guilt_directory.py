from guilt.interfaces.services.guilt_directory import GuiltDirectoryServiceInterface
from guilt.interfaces.services.environment_variables import EnvironmentVariablesServiceInterface
from guilt.services.guilt_directory import GuiltDirectoryService
from tests.mocks.services.environment_variables import MockEnvironmentVariablesService
from guilt.dependencies.injector import DependencyInjector
from pathlib import Path

TEST_HOME_DIR = Path("/home/test")

def test_get_guilt_directory_path() -> None:
  di = DependencyInjector()
  di.register_instance(EnvironmentVariablesServiceInterface, MockEnvironmentVariablesService({}, TEST_HOME_DIR))
  di.bind(GuiltDirectoryServiceInterface, GuiltDirectoryService)
  guilt_directory_service = di.resolve(GuiltDirectoryServiceInterface) # type: ignore[type-abstract]
  
  result = guilt_directory_service.get_guilt_directory_path()
  
  assert isinstance(result, Path)
  assert result.is_relative_to(TEST_HOME_DIR)
  
def test_get_cpu_profiles_config_path() -> None:
  di = DependencyInjector()
  di.register_instance(EnvironmentVariablesServiceInterface, MockEnvironmentVariablesService({}, TEST_HOME_DIR))
  di.bind(GuiltDirectoryServiceInterface, GuiltDirectoryService)
  guilt_directory_service = di.resolve(GuiltDirectoryServiceInterface) # type: ignore[type-abstract]
  
  result = guilt_directory_service.get_cpu_profiles_config_path()
  
  assert isinstance(result, Path)
  assert result.is_relative_to(TEST_HOME_DIR)
  
def test_get_processed_jobs_data_path() -> None:
  di = DependencyInjector()
  di.register_instance(EnvironmentVariablesServiceInterface, MockEnvironmentVariablesService({}, TEST_HOME_DIR))
  di.bind(GuiltDirectoryServiceInterface, GuiltDirectoryService)
  guilt_directory_service = di.resolve(GuiltDirectoryServiceInterface) # type: ignore[type-abstract]
  
  result = guilt_directory_service.get_processed_jobs_data_path()
  
  assert isinstance(result, Path)
  assert result.is_relative_to(TEST_HOME_DIR)
  
def test_get_unprocessed_jobs_data_path() -> None:
  di = DependencyInjector()
  di.register_instance(EnvironmentVariablesServiceInterface, MockEnvironmentVariablesService({}, TEST_HOME_DIR))
  di.bind(GuiltDirectoryServiceInterface, GuiltDirectoryService)
  guilt_directory_service = di.resolve(GuiltDirectoryServiceInterface) # type: ignore[type-abstract]
  
  result = guilt_directory_service.get_unprocessed_jobs_data_path()
  
  assert isinstance(result, Path)
  assert result.is_relative_to(TEST_HOME_DIR)