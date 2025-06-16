from guilt.log import logger
import argparse
import logging
import guilt.commands as commands

level_map = {
  "debug": logging.DEBUG,
  "info": logging.INFO,
  "warning": logging.WARNING,
  "error": logging.ERROR
}

def main():
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
  
  for command_module in commands.ALL_COMMANDS:
    command_module.register_subparser(subparsers)

  args = parser.parse_args()
  
  level = level_map.get(args.log_level, logging.WARNING)
    
  logging.basicConfig(
    level=level,
    format="%(levelname)s [%(name)s]: %(message)s"
  )
  logger.setLevel(level)
  
  args.function(args)