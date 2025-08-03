from guilt.interfaces.command import CommandInterface
from guilt.interfaces.services.user import UserServiceInterface
from guilt.interfaces.services.slurm_accounting import SlurmAccountingServiceInterface
from guilt.interfaces.services.backfill import BackfillServiceInterface
from guilt.interfaces.services.unprocessed_jobs_data import UnprocessedJobsDataServiceInterface

class BackfillCommand(CommandInterface):
  def __init__(
    self,
    user_service: UserServiceInterface,
    slurm_accounting_service: SlurmAccountingServiceInterface,
    backfill_service: BackfillServiceInterface,
    unprocessed_jobs_data_service: UnprocessedJobsDataServiceInterface
  ) -> None:
    self._user_service = user_service
    self._slurm_accounting_service = slurm_accounting_service
    self._backfill_service = backfill_service
    self._unprocessed_jobs_data_service = unprocessed_jobs_data_service

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
    converted_unprocessed_jobs = self._backfill_service.convert_slurm_jobs_to_unprocessed_jobs(all_historical_user_jobs)

    unprocessed_jobs_data = self._unprocessed_jobs_data_service.read_from_file()

    for unprocessed_job in converted_unprocessed_jobs:
      if not unprocessed_job.job_id in unprocessed_jobs_data.jobs.keys():
        unprocessed_jobs_data.jobs[unprocessed_job.job_id] = unprocessed_job

    self._unprocessed_jobs_data_service.write_to_file(unprocessed_jobs_data)