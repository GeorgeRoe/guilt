from abc import ABC, abstractmethod
from pathlib import Path
from datetime import datetime
from typing import Optional
from guilt.models.slurm_batch_test_result import SlurmBatchTestResult

class SlurmBatchServiceInterface(ABC):
  @abstractmethod
  def submit_job(self, file: Path, begin: Optional[datetime]) -> str:
    pass

  @abstractmethod
  def test_job(self, file: Path, begin: Optional[datetime]) -> SlurmBatchTestResult:
    pass