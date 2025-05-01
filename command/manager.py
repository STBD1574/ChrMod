# -*- coding: utf-8 -*-

from .registry import CommandRegistry

class CommandManager:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(CommandManager, cls).__new__(cls)
        return cls.instance

    def __init__(self, registry):
        self.registry = registry # type: CommandRegistry

    def register(self, command):
        self.registry.register(command)

    def get_commands(self):
        return self.registry.get_commands()
    
    def new_exception(self, message):
        return Exception(message)
    
    def init_commands(self):
        from .commands.scripts import ScriptsCommand
        from .commands.help import HelpCommand
        self.register(ScriptsCommand())
        self.register(HelpCommand())