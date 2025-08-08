from abc import ABC, abstractmethod
from guilt.interfaces.models.user import UserInterface

class RepositorySetupStrategyInterface(ABC):
  @abstractmethod
  def execute(self, user: UserInterface) -> bool:
    pass