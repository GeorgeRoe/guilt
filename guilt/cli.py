from guilt.commands import COMMANDS
from guilt.utility.resolve_and_execute_command import resolve_and_execute_command_factory
from guilt.dependencies.injector import DependencyInjector
from guilt.dependencies.default import bind_default_services
from guilt.log import logger
import argparse
import logging

level_map = {
  "debug": logging.DEBUG,
  "info": logging.INFO,
  "warning": logging.WARNING,
  "error": logging.ERROR
}

def main():
  di = DependencyInjector()
  bind_default_services(di)

  parser = argparse.ArgumentParser(
    description="GUILT: Green Usage Impact Logging Tool"
  )
  
  parser.add_argument(
    "--log-level",
    choices=level_map.keys(),
    default="error",
    help="Set the logging level (default: error)"
  )

  subparsers = parser.add_subparsers(dest="command", required=True)
  
  for command in COMMANDS:
    subparser = subparsers.add_parser(command.name())
    subparser.set_defaults(function=resolve_and_execute_command_factory(di, command))
    command.configure_subparser(subparser)

  args = parser.parse_args()
  
  level = level_map.get(str(args.log_level), logging.WARNING)
    
  logging.basicConfig(
    level=level,
    format="%(levelname)s [%(name)s]: %(message)s"
  )
  logger.setLevel(level)
  
  args.function(args)