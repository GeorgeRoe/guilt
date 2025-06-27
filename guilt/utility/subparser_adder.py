from typing import Protocol
from argparse import ArgumentParser

class SubparserAdder(Protocol):
  def add_parser(self, name: str) -> ArgumentParser: ...