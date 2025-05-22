# -*- coding: utf-8 -*-

from .command import Command

class CommandRegistry(object):
    _instance = None

    def __new__(cls):
        """
        Singleton class.
        """
        if cls._instance is None:
            cls._instance = super(CommandRegistry, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self._commands = { } # type: dict[str, Command]

    def register(self, command):
        # type: (Command) -> None
        """
        Register a command.
        """
        if not isinstance(command, Command):
            raise TypeError("command must be an instance of Command")

        self._commands[command.name] = command

    def get_commands(self):
        # type: () -> dict[str, Command]
        """
        Get all registered commands.
        """
        return self._commands.itervalues()
    
    def get_command_by_name(self, name):
        # type: (str) -> Command | None
        """
        Get a command by name.
        """
        return self._commands.get(name)
    
def init():
    from .commands.help import HelpCommand
    from .commands.scripts import ScriptsCommand

    registry = CommandRegistry()
    registry.register(HelpCommand())
    registry.register(ScriptsCommand())
