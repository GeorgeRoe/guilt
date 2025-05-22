import argparse
from guilt.commands import setup_cmd, teardown_cmd, forecast_cmd, config_cmd

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
  config_parser.set_defaults(function=config_cmd)

  args = parser.parse_args()
  args.function()