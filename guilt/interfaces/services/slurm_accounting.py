from abc import ABC, abstractmethod
from guilt.models.slurm_accounting_result import SlurmAccountingResult

class SlurmAccountingServiceInterface(ABC): 
  @abstractmethod
  def get_jobs_with_ids(self, ids: list[str]) -> list[SlurmAccountingResult]:
    pass
  
  @abstractmethod
  def get_users_jobs(self, user: str) -> list[SlurmAccountingResult]:
    pass