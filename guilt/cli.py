from guilt.commands import COMMANDS
from guilt.utility.resolve_and_execute_command import resolve_and_execute_command_factory
from guilt.dependencies.injector import DependencyInjector
from guilt.dependencies.default import bind_default_services
import argparse
import logging

def main():
  di = DependencyInjector()
  bind_default_services(di)

  parser = argparse.ArgumentParser(
    description="GUILT: Green Usage Impact Logging Tool"
  )
  
  subparsers = parser.add_subparsers(dest="command", required=True)
  
  for command in COMMANDS:
    subparser = subparsers.add_parser(command.name())
    subparser.set_defaults(function=resolve_and_execute_command_factory(di, command))
    command.configure_subparser(subparser)

  args = parser.parse_args()
  
  args.function(args)