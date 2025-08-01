from guilt.interfaces.services.cpu_profiles_config import CpuProfilesConfigServiceInterface
from guilt.interfaces.services.user import UserServiceInterface
from guilt.services.cpu_profiles_config import CpuProfilesConfigService
from tests.mocks.services.user import MockUserService
from guilt.dependencies.injector import DependencyInjector
from guilt.models.cpu_profiles_config import CpuProfilesConfig
from guilt.models.cpu_profile import CpuProfile
from guilt.mappers.json import MapToJson
from tests.mocks.models.user import MockUser
from guilt.utility import guilt_user_file_paths
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
  di.register_instance(UserServiceInterface, MockUserService([]))
  di.bind(CpuProfilesConfigServiceInterface, CpuProfilesConfigService)
  cpu_profiles_config_service = di.resolve(CpuProfilesConfigServiceInterface) # type: ignore[type-abstract]
  
  default = cpu_profiles_config_service.get_default()
  
  assert isinstance(default, CpuProfilesConfig)
  
def test_read_from_file(tmp_path: Path) -> None:
  current_user = MockUser(
    "user",
    "Firstname Lastname",
    tmp_path,
    True
  )

  user_cpu_profiles_config_path = guilt_user_file_paths.get_cpu_profiles_config_path(current_user)

  user_cpu_profiles_config_path.parent.mkdir(parents=True, exist_ok=True)

  with user_cpu_profiles_config_path.open("w") as file:
      json.dump(
        MapToJson.from_cpu_profiles_config(DEFAULT_CPU_PROFILES_CONFIG),
        file,
        indent=2
      )
  
  di = DependencyInjector()
  di.register_instance(UserServiceInterface, MockUserService([current_user]))
  di.bind(CpuProfilesConfigServiceInterface, CpuProfilesConfigService)
  cpu_profiles_config_service = di.resolve(CpuProfilesConfigServiceInterface) # type: ignore[type-abstract]
  
  assert cpu_profiles_config_service.read_from_file() == DEFAULT_CPU_PROFILES_CONFIG
   
def test_write_to_file(tmp_path: Path) -> None:
  current_user = MockUser(
    "user",
    "Firstname Lastname",
    tmp_path,
    True
  )

  di = DependencyInjector()
  di.register_instance(UserServiceInterface, MockUserService([current_user]))
  di.bind(CpuProfilesConfigServiceInterface, CpuProfilesConfigService)
  cpu_profiles_config_service = di.resolve(CpuProfilesConfigServiceInterface) # type: ignore[type-abstract]
  
  cpu_profiles_config_service.write_to_file(DEFAULT_CPU_PROFILES_CONFIG)

  user_cpu_profiles_config_path = guilt_user_file_paths.get_cpu_profiles_config_path(current_user)
  with user_cpu_profiles_config_path.open("r") as file:
    data = json.load(file)

  assert isinstance(data, dict)
  assert data == MapToJson.from_cpu_profiles_config(DEFAULT_CPU_PROFILES_CONFIG)