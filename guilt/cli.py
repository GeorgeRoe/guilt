from guilt.commands import setup_cmd, teardown_cmd, forecast_cmd, config_cmd, batch_cmd, process_cmd, report_cmd, backfill_cmd, friends_cmd
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

  setup_parser = subparsers.add_parser("setup")
  setup_parser.set_defaults(function=setup_cmd)

  teardown_parser = subparsers.add_parser("teardown")
  teardown_parser.set_defaults(function=teardown_cmd)

  forecast_parser = subparsers.add_parser("forecast")
  forecast_parser.set_defaults(function=forecast_cmd)

  config_parser = subparsers.add_parser("config")
  config_parser.add_argument(
      "action",
      help="What to do with the config",
      choices=["add", "remove", "update", "show"]
  )
  config_parser.add_argument(
      "type",
      help="Type of config to modify",
      choices=["cpu_profile"]
  )
  config_parser.set_defaults(function=config_cmd)

  batch_parser = subparsers.add_parser("batch")
  batch_parser.add_argument("input", help="Input file or argument for batch command")
  batch_parser.set_defaults(function=batch_cmd)
  
  process_parser = subparsers.add_parser("process")
  process_parser.set_defaults(function=process_cmd)
  
  report_parser = subparsers.add_parser("report")
  report_parser.add_argument(
    "--group-by",
    help="How the report should be grouped by",
    choices=["day", "week", "month", "year"],
    default="month"
  )
  report_parser.set_defaults(function=report_cmd)
  
  backfill_parser = subparsers.add_parser("backfill")
  backfill_parser.set_defaults(function=backfill_cmd)
  
  friends_parser = subparsers.add_parser("friends")
  friends_parser.set_defaults(function=friends_cmd)

  args = parser.parse_args()
  
  level = level_map.get(args.log_level, logging.WARNING)
    
  logging.basicConfig(
    level=level,
    format="%(levelname)s [%(name)s]: %(message)s"
  )
  logger.setLevel(level)
  
  args.function(args)