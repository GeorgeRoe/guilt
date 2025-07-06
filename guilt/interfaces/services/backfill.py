from abc import ABC, abstractmethod
from guilt.models.slurm_accounting_result import SlurmAccountingResult
from guilt.models.unprocessed_job import UnprocessedJob

class BackfillServiceInterface(ABC):
  @abstractmethod
  def convert_slurm_jobs_to_unprocessed_jobs(self, slurm_accounting_results: list[SlurmAccountingResult]) -> list[UnprocessedJob]:
    pass