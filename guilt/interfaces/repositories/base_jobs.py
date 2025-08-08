from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional, Sequence

T = TypeVar("T")

class BaseJobsRepositoryInterface(ABC, Generic[T]):
  @abstractmethod
  def get(self, job_id: str) -> Optional[T]:
    pass

  @abstractmethod
  def get_all(self) -> Sequence[T]:
    pass

  @abstractmethod
  def upsert(self, job: T) -> None:
    pass

  @abstractmethod
  def delete(self, job_id: str) -> None:
    pass

  @abstractmethod
  def save(self) -> bool:
    pass