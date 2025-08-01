from guilt.interfaces.services.cpu_profiles_config import CpuProfilesConfigServiceInterface
from guilt.interfaces.services.guilt_directory import GuiltDirectoryServiceInterface
from guilt.services.cpu_profiles_config import CpuProfilesConfigService
from tests.mocks.services.guilt_directory import MockGuiltDirectoryService
from guilt.dependencies.injector import DependencyInjector
from guilt.models.cpu_profiles_config import CpuProfilesConfig
from guilt.models.cpu_profile import CpuProfile
from guilt.mappers.json import MapToJson
from pathlib import Path
import json

default_profile = CpuProfile("AMD EPYC 9654", 360, 96)
    
profiles = [
  default_profile,
  CpuProfile("AMD EPYC 7502", 180, 32),
  CpuProfile("AMD EPYC 7742", 225, 64),
  CpuProfile("AMD EPYC 7543P", 225, 32)
]
  
DEFAULT_CPU_PROFILES_CONFIG = CpuProfilesConfig(default_profile, {profile.name: profile for profile in profiles})
  
def test_get_default(tmp_path: Path) -> None:
  di = DependencyInjector()
  di.register_instance(GuiltDirectoryServiceInterface, MockGuiltDirectoryService(tmp_path))
  di.bind(CpuProfilesConfigServiceInterface, CpuProfilesConfigService)
  cpu_profiles_config_service = di.resolve(CpuProfilesConfigServiceInterface) # type: ignore[type-abstract]
  
  default = cpu_profiles_config_service.get_default()
  
  assert isinstance(default, CpuProfilesConfig)
  
def test_read_from_file(tmp_path: Path) -> None:
  mock_guilt_directory_service = MockGuiltDirectoryService(tmp_path)
  mock_guilt_directory_service.get_guilt_directory_path().mkdir(parents=True, exist_ok=True)
  with mock_guilt_directory_service.get_cpu_profiles_config_path().open("w") as file:
      json.dump(
        MapToJson.from_cpu_profiles_config(DEFAULT_CPU_PROFILES_CONFIG),
        file,
        indent=2
      )
  
  di = DependencyInjector()
  di.register_instance(GuiltDirectoryServiceInterface, mock_guilt_directory_service)
  di.bind(CpuProfilesConfigServiceInterface, CpuProfilesConfigService)
  cpu_profiles_config_service = di.resolve(CpuProfilesConfigServiceInterface) # type: ignore[type-abstract]
  
  assert cpu_profiles_config_service.read_from_file() == DEFAULT_CPU_PROFILES_CONFIG
   
def test_write_to_file(tmp_path: Path) -> None:
  mock_guilt_directory_service = MockGuiltDirectoryService(tmp_path)

  di = DependencyInjector()
  di.register_instance(GuiltDirectoryServiceInterface, mock_guilt_directory_service)
  di.bind(CpuProfilesConfigServiceInterface, CpuProfilesConfigService)
  cpu_profiles_config_service = di.resolve(CpuProfilesConfigServiceInterface) # type: ignore[type-abstract]
  
  cpu_profiles_config_service.write_to_file(DEFAULT_CPU_PROFILES_CONFIG)

  with mock_guilt_directory_service.get_cpu_profiles_config_path().open("r") as file:
    data = json.load(file)

  assert isinstance(data, dict)
  assert data == MapToJson.from_cpu_profiles_config(DEFAULT_CPU_PROFILES_CONFIG)