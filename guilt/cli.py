import argparse
from guilt.commands import setup_cmd, teardown_cmd, forecast_cmd, config_cmd, batch_cmd, process_cmd

def main():
  parser = argparse.ArgumentParser(
    description="GUILT: Green Usage Impact Logging Tool"
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

  args = parser.parse_args()
  args.function(args)