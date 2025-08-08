from guilt.interfaces.models.cpu_profile import CpuProfileInterface
from abc import ABC, abstractmethod
from typing import Optional, Sequence

class CpuProfilesRepositoryInterface (ABC):
  @abstractmethod
  def get(self, name: str) -> Optional[CpuProfileInterface]:
    pass

  @abstractmethod
  def get_all(self) -> Sequence[CpuProfileInterface]:
    pass

  @abstractmethod
  def upsert(self, cpu_profile: CpuProfileInterface) -> None:
    pass

  @abstractmethod
  def delete(self, name: str) -> None:
    pass

  @abstractmethod
  def save(self) -> bool:
    pass