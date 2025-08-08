from abc import ABC, abstractmethod

class CpuProfileInterface(ABC):
  @property
  @abstractmethod
  def name(self) -> str:
    pass

  @property
  @abstractmethod
  def tdp(self) -> float:
    pass

  @property
  @abstractmethod
  def cores(self) -> int:
    pass