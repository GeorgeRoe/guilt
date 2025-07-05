from abc import ABC, abstractmethod
from guilt.models.ip_info_result import IpInfoResult

class IpInfoServiceInterface(ABC):
  @abstractmethod
  def get_ip_info(self) -> IpInfoResult:
    pass