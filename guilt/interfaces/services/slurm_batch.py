from abc import ABC, abstractmethod
from pathlib import Path

class SlurmBatchServiceInterface(ABC):
  @abstractmethod
  def submit_job(self, file: Path) -> str:
    pass