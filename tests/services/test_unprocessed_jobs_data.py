from guilt.interfaces.services.unprocessed_jobs_data import UnprocessedJobsDataServiceInterface
from guilt.interfaces.services.user import UserServiceInterface
from guilt.services.unprocessed_jobs_data import UnprocessedJobsDataService
from tests.mocks.services.user import MockUserService
from guilt.dependencies.injector import DependencyInjector
from guilt.models.unprocessed_jobs_data import UnprocessedJobsData
from guilt.models.unprocessed_job import UnprocessedJob
from guilt.models.cpu_profile import CpuProfile
from tests.mocks.models.user import MockUser
from guilt.utility import guilt_user_file_paths
from guilt.mappers.json import MapToJson
from pathlib import Path
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

def test_read_from_file(tmp_path: Path) -> None:
  current_user = MockUser(
    "user",
    "Firstname Lastname",
    tmp_path,
    True
  )

  user_unprocessed_jobs_data_path = guilt_user_file_paths.get_unprocessed_jobs_data_path(current_user)

  with user_unprocessed_jobs_data_path.open("w") as file:
    json.dump(
      MapToJson.from_unprocessed_jobs_data(EXAMPLE_DATA),
      file,
      indent=2
    )

  di = DependencyInjector()
  di.register_instance(UserServiceInterface, MockUserService([current_user]))
  di.bind(UnprocessedJobsDataServiceInterface, UnprocessedJobsDataService)
  unprocessed_jobs_data_service = di.resolve(UnprocessedJobsDataServiceInterface) # type: ignore[type-abstract]
  
  assert unprocessed_jobs_data_service.read_from_file() == EXAMPLE_DATA
  
def test_write_to_file(tmp_path: Path) -> None:
  current_user = MockUser(
    "user",
    "Firstname Lastname",
    tmp_path,
    True
  )
  
  di = DependencyInjector()
  di.register_instance(UserServiceInterface, MockUserService([current_user]))
  di.bind(UnprocessedJobsDataServiceInterface, UnprocessedJobsDataService)
  unprocessed_jobs_data_service = di.resolve(UnprocessedJobsDataServiceInterface) # type: ignore[type-abstract]
  
  unprocessed_jobs_data_service.write_to_file(EXAMPLE_DATA)

  user_unprocessed_jobs_data_path = guilt_user_file_paths.get_unprocessed_jobs_data_path(current_user)
  with user_unprocessed_jobs_data_path.open("r") as file:
    data = json.load(file)
  
  assert isinstance(data, dict)
  assert data == MapToJson.from_unprocessed_jobs_data(EXAMPLE_DATA)