from abc import ABC, abstractmethod
from guilt.models.lazy_ip_info_result import LazyIpInfoResult

class IpInfoServiceInterface(ABC):
  @abstractmethod
  def get_ip_info(self) -> LazyIpInfoResult:
    pass