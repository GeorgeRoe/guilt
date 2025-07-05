from abc import ABC, abstractmethod
from guilt.models.get_entires_password_result import GetEntriesPasswordResult

class GetEntriesPasswordServiceInterface(ABC):
  @abstractmethod
  def get_entries(self) -> list[GetEntriesPasswordResult]:
    pass