from guilt.interfaces.command import CommandInterface
from guilt.interfaces.services.user import UserServiceInterface
from guilt.interfaces.services.slurm_accounting import SlurmAccountingServiceInterface
from guilt.interfaces.services.unprocessed_jobs_data import UnprocessedJobsDataServiceInterface
from guilt.interfaces.services.cpu_profiles_config import CpuProfilesConfigServiceInterface
from guilt.mappers import map_to

class BackfillCommand(CommandInterface):
  def __init__(
    self,
    user_service: UserServiceInterface,
    slurm_accounting_service: SlurmAccountingServiceInterface,
    unprocessed_jobs_data_service: UnprocessedJobsDataServiceInterface,
    cpu_profiles_config_service: CpuProfilesConfigServiceInterface
  ) -> None:
    self._user_service = user_service
    self._slurm_accounting_service = slurm_accounting_service
    self._unprocessed_jobs_data_service = unprocessed_jobs_data_service
    self._cpu_profiles_config_service = cpu_profiles_config_service

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
    
    all_historical_user_jobs = self._slurm_accounting_service.get_jobs_submitted_by_username(current_user.username)

    default_cpu_profile = self._cpu_profiles_config_service.read_from_file().default

    converted_unprocessed_jobs = [
      map_to.unprocessed_job.from_slurm_accounting_result(result, default_cpu_profile)
      for result in all_historical_user_jobs
    ]

    unprocessed_jobs_data = self._unprocessed_jobs_data_service.read_from_file()

    for unprocessed_job in converted_unprocessed_jobs:
      if not unprocessed_job.job_id in unprocessed_jobs_data.jobs.keys():
        unprocessed_jobs_data.jobs[unprocessed_job.job_id] = unprocessed_job

    self._unprocessed_jobs_data_service.write_to_file(unprocessed_jobs_data)