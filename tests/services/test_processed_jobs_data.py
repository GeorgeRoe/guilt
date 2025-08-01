from guilt.interfaces.services.processed_jobs_data import ProcessedJobsDataServiceInterface
from guilt.interfaces.services.user import UserServiceInterface
from guilt.services.processed_jobs_data import ProcessedJobsDataService
from tests.mocks.services.user import MockUserService
from guilt.dependencies.injector import DependencyInjector
from guilt.models.processed_jobs_data import ProcessedJobsData
from guilt.models.processed_job import ProcessedJob
from guilt.models.cpu_profile import CpuProfile
from guilt.mappers.json import MapToJson
from tests.mocks.models.user import MockUser
from guilt.utility import guilt_user_file_paths
from datetime import datetime
from pathlib import Path
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

def test_read_from_file(tmp_path: Path) -> None:
  current_user = MockUser(
    "user",
    "Firstname Lastname",
    tmp_path,
    True
  )

  user_processed_jobs_data_path = guilt_user_file_paths.get_processed_jobs_data_path(current_user)

  with user_processed_jobs_data_path.open("w") as file:
    json.dump(
      MapToJson.from_processed_jobs_data(EXAMPLE_DATA),
      file,
      indent=2
    )

  di = DependencyInjector()
  di.register_instance(UserServiceInterface, MockUserService([current_user]))
  di.bind(ProcessedJobsDataServiceInterface, ProcessedJobsDataService)
  processed_jobs_data_service = di.resolve(ProcessedJobsDataServiceInterface) # type: ignore[type-abstract]
  
  assert processed_jobs_data_service.read_from_file() == EXAMPLE_DATA
  
def test_write_to_file(tmp_path: Path) -> None:
  current_user = MockUser(
    "user",
    "Firstname Lastname",
    tmp_path,
    True
  )
  
  di = DependencyInjector()
  di.register_instance(UserServiceInterface, MockUserService([current_user]))
  di.bind(ProcessedJobsDataServiceInterface, ProcessedJobsDataService)
  processed_jobs_data_service = di.resolve(ProcessedJobsDataServiceInterface) # type: ignore[type-abstract]
  
  processed_jobs_data_service.write_to_file(EXAMPLE_DATA)

  user_processed_jobs_data_path = guilt_user_file_paths.get_processed_jobs_data_path(current_user)
  with user_processed_jobs_data_path.open("r") as file:
    data = json.load(file)
  
  assert isinstance(data, dict)
  assert data == MapToJson.from_processed_jobs_data(EXAMPLE_DATA)