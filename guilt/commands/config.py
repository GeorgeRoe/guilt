from guilt.config.cpu_profiles import CpuProfilesConfig, CpuProfile
from argparse import _SubParsersAction, ArgumentParser, Namespace # type: ignore

def execute(args: Namespace):
  if args.type == "cpu_profile":
    cpu_profiles_config = CpuProfilesConfig.from_file()

    if args.action == "add":
      print("Add a new CPU profile")
      name = input("name: ")
      tdp = int(input("tdp: "))
      cores = int(input("cores: "))
      profile = CpuProfile(name, tdp, cores)
      result = cpu_profiles_config.add_profile(profile)
      if not result:
        print("Failed to add CPU profile")
    elif args.action == "remove":
      print("Remove a new CPU profile")
      name = input("name: ")
      profile = cpu_profiles_config.get_profile(name)
      if profile:
        cpu_profiles_config.remove_profile(profile)
      else:
        print(f"Profile '{name}' doesn't exist")
    elif args.action == "update":
      print("Update a CPU profile")
      name = input("name: ")
      profile = cpu_profiles_config.get_profile(name)
      if profile is None:
        print(f"Profile '{name}' doesn't exist")
        return
      tdp = int(input(f"tdp (default={profile.tdp}): ")) or profile.tdp
      cores = int(input("cores: "))
      profile = CpuProfile(name, tdp, cores)
      print(profile)
      result = cpu_profiles_config.add_profile(profile)
      if not result:
        print("Failed to add CPU Profile")
    elif args.action == "show":
      print("CPU Profiles:")
      for profile in cpu_profiles_config.profiles.values():
        print(f"{profile.name} -> TDP: {profile.tdp} | cores: {profile.cores}")
        
def register_subparser(subparsers: _SubParsersAction[ArgumentParser]):
  subparser = subparsers.add_parser("config")
  subparser.add_argument(
    "action",
    help="What to do with the config",
    choices=["add", "remove", "update", "show"]
  )
  subparser.add_argument(
    "type",
    help="Type of config to modify",
    choices=["cpu_profile"]
  )
  subparser.set_defaults(function=execute)