from guilt.interfaces.command import CommandInterface
from guilt.dependencies.injector import DependencyInjector
from argparse import Namespace
from typing import Callable

def resolve_and_execute_command_factory(
  di: DependencyInjector,
  command: type[CommandInterface],
) -> Callable[[Namespace], None]:
  def resolve_and_execute_command(args: Namespace) -> None:
    di.bind(CommandInterface, command)
    command_instance = di.resolve(CommandInterface) # type: ignore[type-abstract]
    command_instance.execute(args)

  return resolve_and_execute_command