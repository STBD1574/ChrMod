# -*- coding: utf-8 -*-
#v3主要是彻底重写了command，之前的太难看了

commands = [] #type: list[Command]

class Command:
    def __init__(self, name, description, usageMessage="", aliases=[], **args):
        self.name = name #type: str
        self.description = description #type: str
        self.usageMessage = usageMessage #type: str
        self.aliases = aliases #type: list[str]
        self.args = args #type: dict[str, any]

    def Execute(self, label, args): #type: (str, list[str]) -> bool
        print("请重写该方法")

def InitCommands():
    # 同样的，command也这么做
    from ChrMod.Command.Commands.Teleport import Teleport
    from ChrMod.Command.Commands.Help import Help
    from ChrMod.Command.Commands.Execute import Execute
    from ChrMod.Command.Commands.Platform import Platform
    from ChrMod.Command.Commands.InputMode import InputMode
    from ChrMod.Command.Commands.Config import Config
    from ChrMod.Command.Commands.Bind import Bind
    # Init
    commands.append(Teleport())
    commands.append(Help())
    commands.append(Execute())
    commands.append(Platform())
    commands.append(InputMode())
    commands.append(Config())
    commands.append(Bind())

def DispatchCommand(command, label, args): #type: (Command, str, list[str]) -> None
    return command.Execute(label, args)
