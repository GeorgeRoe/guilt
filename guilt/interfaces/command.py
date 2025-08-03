from abc import ABC, abstractmethod
from argparse import Namespace
from argparse import ArgumentParser

class CommandInterface(ABC):
  @staticmethod
  @abstractmethod
  def name() -> str:
    pass

  @staticmethod
  @abstractmethod
  def configure_subparser(subparser: ArgumentParser) -> None:
    pass

  @abstractmethod
  def execute(self, args: Namespace) -> None:
    pass