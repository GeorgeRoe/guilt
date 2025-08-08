from guilt.interfaces.command import CommandInterface
from guilt.interfaces.services.user import UserServiceInterface
from guilt.interfaces.services.repository_factory import RepositoryFactoryServiceInterface
from guilt.utility import slurm_accounting
from guilt.models.unprocessed_job import UnprocessedJob
from datetime import datetime

class BackfillCommand(CommandInterface):
  def __init__(
    self,
    user_service: UserServiceInterface,
    repository_factory_service: RepositoryFactoryServiceInterface
  ) -> None:
    self._user_service = user_service
    self._repository_factory_service = repository_factory_service

  @staticmethod
  def name() -> str:
    return "backfill"

  @staticmethod
  def configure_subparser(_) -> None:
    pass

  def execute(self, _) -> None:
    current_user = self._user_service.get_current_user()

    if current_user is None:
      raise RuntimeError("No user is currently logged in. Please log in to continue.")
    
    all_historical_user_jobs = slurm_accounting.run(
      user=current_user.username,
      since=datetime(1970, 1, 1),
    )

    default_cpu_profile = self._repository_factory_service.get_settings_repository(current_user).get_default_cpu_profile()
    if default_cpu_profile is None:
      print("You must set a default CPU profile before running the backfill command.")
      return

    converted_unprocessed_jobs: list[UnprocessedJob] = [
      UnprocessedJob(
        job_id=result.job_id,
        cpu_profile=default_cpu_profile
      )
      for result in all_historical_user_jobs
    ]

    unprocessed_jobs_repository = self._repository_factory_service.get_unprocessed_jobs_repository(current_user)

    for unprocessed_job in converted_unprocessed_jobs:
      unprocessed_jobs_repository.upsert(unprocessed_job)

    unprocessed_jobs_repository.save()