from .backfill import BackfillCommand
from .batch import BatchCommand
from .forecast import ForecastCommand
from .friends import FriendsCommand
from .process import ProcessCommand
from .report import ReportCommand
from .setup import SetupCommand
from .teardown import TeardownCommand
from guilt.interfaces.command import CommandInterface
from typing import Iterable

COMMANDS: Iterable[type[CommandInterface]] = [
  BackfillCommand,
  BatchCommand,
  ForecastCommand,
  FriendsCommand,
  ProcessCommand,
  ReportCommand,
  SetupCommand,
  TeardownCommand,
]