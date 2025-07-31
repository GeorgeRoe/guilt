from abc import ABC, abstractmethod
from guilt.models.lazy_slurm_accounting_result import LazySlurmAccountingResult

class SlurmAccountingServiceInterface(ABC): 
  @abstractmethod
  def get_jobs_with_ids(self, ids: list[str]) -> list[LazySlurmAccountingResult]:
    pass
  
  @abstractmethod
  def get_users_jobs(self, user: str) -> list[LazySlurmAccountingResult]:
    pass
  
  @abstractmethod
  def get_current_users_jobs(self) -> list[LazySlurmAccountingResult]:
    pass