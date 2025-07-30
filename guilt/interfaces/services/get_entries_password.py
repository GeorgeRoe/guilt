from abc import ABC, abstractmethod
from guilt.models.lazy_get_entries_password_result import LazyGetEntriesPasswordResult

class GetEntriesPasswordServiceInterface(ABC):
  @abstractmethod
  def get_entries(self) -> list[LazyGetEntriesPasswordResult]:
    pass