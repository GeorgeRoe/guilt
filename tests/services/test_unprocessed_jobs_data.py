from guilt.interfaces.services.unprocessed_jobs_data import UnprocessedJobsDataServiceInterface
from guilt.interfaces.services.file_system import FileSystemServiceInterface
from guilt.interfaces.services.guilt_directory import GuiltDirectoryServiceInterface
from guilt.services.unprocessed_jobs_data import UnprocessedJobsDataService
from tests.mocks.services.file_system_service import MockFileSystemService, FileSystemNode, add_path_to_file_system, get_node_at_path
from tests.mocks.services.guilt_directory import MockGuiltDirectoryService, TestGuiltDirectories
from guilt.dependencies.injector import DependencyInjector
from guilt.models.unprocessed_jobs_data import UnprocessedJobsData
from guilt.models.unprocessed_job import UnprocessedJob
from guilt.models.cpu_profile import CpuProfile
from guilt.mappers.json import MapToJson
import json

_job_list: list[UnprocessedJob] = [
  UnprocessedJob(
    job_id="1",
    cpu_profile=CpuProfile(
      name="TestProfile",
      cores=4,
      tdp=10
    )
  )
]

EXAMPLE_DATA = UnprocessedJobsData({job.job_id: job for job in _job_list})

def test_read_from_file() -> None:
  test_directories = TestGuiltDirectories()
  fs: FileSystemNode = {}
  add_path_to_file_system(fs, test_directories.unprocessed_jobs_data, json.dumps(MapToJson.from_unprocessed_jobs_data(EXAMPLE_DATA)))
  
  di = DependencyInjector()
  di.register_instance(FileSystemServiceInterface, MockFileSystemService(fs))
  di.register_instance(GuiltDirectoryServiceInterface, MockGuiltDirectoryService(test_directories))
  di.bind(UnprocessedJobsDataServiceInterface, UnprocessedJobsDataService)
  unprocessed_jobs_data_service = di.resolve(UnprocessedJobsDataServiceInterface) # type: ignore[type-abstract]
  
  assert unprocessed_jobs_data_service.read_from_file() == EXAMPLE_DATA
  
def test_write_to_file() -> None:
  test_directories = TestGuiltDirectories()
  fs: FileSystemNode = {}
  
  di = DependencyInjector()
  di.register_instance(FileSystemServiceInterface, MockFileSystemService(fs))
  di.register_instance(GuiltDirectoryServiceInterface, MockGuiltDirectoryService(test_directories))
  di.bind(UnprocessedJobsDataServiceInterface, UnprocessedJobsDataService)
  unprocessed_jobs_data_service = di.resolve(UnprocessedJobsDataServiceInterface) # type: ignore[type-abstract]
  
  unprocessed_jobs_data_service.write_to_file(EXAMPLE_DATA)
  contents = get_node_at_path(fs, test_directories.unprocessed_jobs_data)
  
  assert isinstance(contents, str)
  assert json.loads(contents) == MapToJson.from_unprocessed_jobs_data(EXAMPLE_DATA)