from abc import ABC, abstractmethod
from guilt.models.lazy_slurm_accounting_result import LazySlurmAccountingResult
from guilt.models.unprocessed_job import UnprocessedJob

class BackfillServiceInterface(ABC):
  @abstractmethod
  def convert_slurm_jobs_to_unprocessed_jobs(self, slurm_accounting_results: list[LazySlurmAccountingResult]) -> list[UnprocessedJob]:
    pass