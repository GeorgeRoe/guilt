from guilt.interfaces.services.processed_jobs_data import ProcessedJobsDataServiceInterface
from guilt.interfaces.services.file_system import FileSystemServiceInterface
from guilt.interfaces.services.guilt_directory import GuiltDirectoryServiceInterface
from guilt.services.processed_jobs_data import ProcessedJobsDataService
from tests.mocks.services.file_system_service import MockFileSystemService, FileSystemNode, add_path_to_file_system, get_node_at_path
from tests.mocks.services.guilt_directory import MockGuiltDirectoryService, TestGuiltDirectories
from guilt.dependencies.injector import DependencyInjector
from guilt.models.processed_jobs_data import ProcessedJobsData
from guilt.models.processed_job import ProcessedJob
from guilt.models.cpu_profile import CpuProfile
from guilt.mappers.json import MapToJson
from datetime import datetime
import json

_job_list: list[ProcessedJob] = [
  ProcessedJob(
    start=datetime(2025, 1, 1, 1),
    end=datetime(2025, 1, 1, 2),
    job_id="1",
    cpu_profile=CpuProfile(
      name="TestProfile",
      cores=4,
      tdp=10
    ),
    energy=40,
    emissions=10,
    generation_mix={
      "solar": 50,
      "wind": 25,
      "other": 25
    }
  )
]

EXAMPLE_DATA = ProcessedJobsData({job.job_id: job for job in _job_list})

def test_read_from_file() -> None:
  test_directories = TestGuiltDirectories()
  fs: FileSystemNode = {}
  add_path_to_file_system(fs, test_directories.processed_jobs_data, json.dumps(MapToJson.from_processed_jobs_data(EXAMPLE_DATA)))
  
  di = DependencyInjector()
  di.register_instance(FileSystemServiceInterface, MockFileSystemService(fs))
  di.register_instance(GuiltDirectoryServiceInterface, MockGuiltDirectoryService(test_directories))
  di.bind(ProcessedJobsDataServiceInterface, ProcessedJobsDataService)
  processed_jobs_data_service = di.resolve(ProcessedJobsDataServiceInterface) # type: ignore[type-abstract]
  
  assert processed_jobs_data_service.read_from_file() == EXAMPLE_DATA
  
def test_write_to_file() -> None:
  test_directories = TestGuiltDirectories()
  fs: FileSystemNode = {}
  
  di = DependencyInjector()
  di.register_instance(FileSystemServiceInterface, MockFileSystemService(fs))
  di.register_instance(GuiltDirectoryServiceInterface, MockGuiltDirectoryService(test_directories))
  di.bind(ProcessedJobsDataServiceInterface, ProcessedJobsDataService)
  processed_jobs_data_service = di.resolve(ProcessedJobsDataServiceInterface) # type: ignore[type-abstract]
  
  processed_jobs_data_service.write_to_file(EXAMPLE_DATA)
  contents = get_node_at_path(fs, test_directories.processed_jobs_data)
  
  assert isinstance(contents, str)
  assert json.loads(contents) == MapToJson.from_processed_jobs_data(EXAMPLE_DATA)