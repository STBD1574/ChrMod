# -*- coding: utf-8 -*-

from ..lib import shlex

def parse_command(command):
    # type: (str) -> tuple[str, list[str]]
    """
    Parses a command string into a tuple of command name and arguments.
    """
    i = 0
    while i < len(command) and command[i] == " ":
        i += 1

    j = i
    while j < len(command) and command[j] != " ":
        j += 1

    command_name = command[i:j]

    arg_str = command[j:].lstrip()
    command_args = shlex.split(arg_str) if arg_str else []

    return command_name.lower(), command_args
