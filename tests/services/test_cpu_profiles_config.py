from guilt.interfaces.services.cpu_profiles_config import CpuProfilesConfigServiceInterface
from guilt.interfaces.services.file_system import FileSystemServiceInterface
from guilt.interfaces.services.guilt_directory import GuiltDirectoryServiceInterface
from guilt.services.cpu_profiles_config import CpuProfilesConfigService
from tests.mocks.services.file_system_service import MockFileSystemService, FileSystemNode, add_path_to_file_system, get_node_at_path
from tests.mocks.services.guilt_directory import MockGuiltDirectoryService, TestGuiltDirectories
from guilt.dependencies.injector import DependencyInjector
from guilt.models.cpu_profiles_config import CpuProfilesConfig
from guilt.models.cpu_profile import CpuProfile
from guilt.mappers.json import MapToJson
import json

default_profile = CpuProfile("AMD EPYC 9654", 360, 96)
    
profiles = [
  default_profile,
  CpuProfile("AMD EPYC 7502", 180, 32),
  CpuProfile("AMD EPYC 7742", 225, 64),
  CpuProfile("AMD EPYC 7543P", 225, 32)
]
  
DEFAULT_CPU_PROFILES_CONFIG = CpuProfilesConfig(default_profile, {profile.name: profile for profile in profiles})
  
def test_get_default() -> None:
  di = DependencyInjector()
  di.register_instance(FileSystemServiceInterface, MockFileSystemService())
  di.register_instance(GuiltDirectoryServiceInterface, MockGuiltDirectoryService())
  di.bind(CpuProfilesConfigServiceInterface, CpuProfilesConfigService)
  cpu_profiles_config_service = di.resolve(CpuProfilesConfigServiceInterface) # type: ignore[type-abstract]
  
  default = cpu_profiles_config_service.get_default()
  
  assert isinstance(default, CpuProfilesConfig)
  
def test_read_from_file() -> None:
  test_directories = TestGuiltDirectories()
  fs: FileSystemNode = {}
  add_path_to_file_system(fs, test_directories.cpu_profiles_config, json.dumps(MapToJson.from_cpu_profiles_config(DEFAULT_CPU_PROFILES_CONFIG)))
  
  di = DependencyInjector()
  di.register_instance(GuiltDirectoryServiceInterface, MockGuiltDirectoryService(test_directories))
  di.register_instance(FileSystemServiceInterface, MockFileSystemService(fs))
  di.bind(CpuProfilesConfigServiceInterface, CpuProfilesConfigService)
  cpu_profiles_config_service = di.resolve(CpuProfilesConfigServiceInterface) # type: ignore[type-abstract]
  
  assert cpu_profiles_config_service.read_from_file() == DEFAULT_CPU_PROFILES_CONFIG
   
def test_write_to_file() -> None:
  test_directories = TestGuiltDirectories()
  fs: FileSystemNode = {}
  
  di = DependencyInjector()
  di.register_instance(GuiltDirectoryServiceInterface, MockGuiltDirectoryService(test_directories))
  di.register_instance(FileSystemServiceInterface, MockFileSystemService(fs))
  di.bind(CpuProfilesConfigServiceInterface, CpuProfilesConfigService)
  cpu_profiles_config_service = di.resolve(CpuProfilesConfigServiceInterface) # type: ignore[type-abstract]
  
  cpu_profiles_config_service.write_to_file(DEFAULT_CPU_PROFILES_CONFIG)
  contents = get_node_at_path(fs, test_directories.cpu_profiles_config)

  assert isinstance(contents, str)
  assert json.loads(contents) == MapToJson.from_cpu_profiles_config(DEFAULT_CPU_PROFILES_CONFIG)