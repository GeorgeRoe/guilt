from guilt.log import logger
from pathlib import Path
from argparse import Namespace
from guilt.utility.subparser_adder import SubparserAdder
from guilt.registries.service import ServiceRegistry
from guilt.interfaces.models.user import UserInterface
from guilt.utility.has_guilt_installed import has_guilt_installed
from typing import Sequence

def execute(services: ServiceRegistry, args: Namespace):
  friends: Sequence[UserInterface] = [
    user
    for user
    in services.user.get_all_users()
    if has_guilt_installed(user)
  ]

  if len(friends) == 0:
    print("You are the only one using GUILT! :(")
    return
  
  print("Here are the other people using GUILT on this system:")
  [print(f"{friend.username} -> {friend.info}") for friend in friends]

def register_subparser(subparsers: SubparserAdder):
  subparser = subparsers.add_parser("friends")
  subparser.set_defaults(function=execute)