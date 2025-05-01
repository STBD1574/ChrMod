# -*- coding: utf-8 -*-

from .command import Command

from typing import Dict # typing

_instance = None

class CommandRegistry:
    def __new__(cls):
        global _instance
        if _instance is None:
            _instance = super().__new__(cls)
        return _instance

    def __init__(self):
        self._commands = { } # type: Dict[str, Command]

    def register(self, command):
        # type: (Command) -> None
        """
        Register a command.
        """
        if not isinstance(command, Command):
            raise TypeError("command must be an instance of Command")

        self._commands[command.name] = command

    def get_commands(self):
        # type: () -> Dict[str, Command]
        """
        Get all registered commands.
        """
        return self._commands.itervalues()
    
    