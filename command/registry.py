# -*- coding: utf-8 -*-

import traceback
from .command import Command
from ..api import client
from ..lib import shlex

class Registry:
    def __init__(self):
        self.commands = [ ]       # type: list[Command]
        self.nameToCommands = { } # type: dict[str, Command]
        self.prefix = '.'

    def Register(self, command): # type: (Command) -> None
        self.commands.append(command)
        self.nameToCommands[command.name] = command

        for alias in command.aliases:
            self.nameToCommands[alias] = command

    def Execute(self, string): # type: (str) -> None
        args = shlex.split(string) # type: list[str]
        if not args:
            client.DisplayClientMessage("{}Unknown command, plaese type {}help for help.".format(client.MESSAGE_PREFIX, self.prefix))
            return

        if args[0].lower() not in self.nameToCommands:
            return
        
        command = self.nameToCommands[args[0].lower()]
        try:
            if command.Execute(args[1:]) is False:
                client.DisplayClientMessage("{}Usage: {}.".format(client.MESSAGE_PREFIX, command.usageMessage))
        except Exception:
            client.DisplayClientMessage("{}Exception: {}".format(client.MESSAGE_PREFIX, traceback.format_exc()))
            return

        client.DisplayClientMessage("{}Unknown command: '{}', plaese type {}help for help.".format(client.MESSAGE_PREFIX, string, self.prefix))

registry = Registry()

def GetRegistry(): # type: () -> Registry
    return registry

def InitCommands(): # type: () -> None
    from commands.help import Help
    from commands.platform import Platform
    from commands.inputmode import InputMode
    from commands.scripts import Scripts
    from commands.toggle import Toggle
    from commands.setting import Setting
    from commands.modules import Modules
    from commands.bind import Bind
    from commands.teleport import Teleport
    from commands.playsound import PlaySound
    registry.Register(Help())
    registry.Register(Platform())
    registry.Register(InputMode())
    registry.Register(Scripts())
    registry.Register(Toggle())
    registry.Register(Setting())
    registry.Register(Modules())
    registry.Register(Bind())
    registry.Register(Teleport())
    registry.Register(PlaySound())