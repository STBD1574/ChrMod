# -*- coding: utf-8 -*-
from ChrMod.Command.CommandManager import Command
from ChrMod.Command.CommandManager import commands
import ChrMod.Module.ModuleManager as ModuleManager
import ChrMod.Api as Api

class Help(Command):
    def __init__(self):
        Command.__init__(self, "help", "获取帮助。", ".help", [])

    def Execute(self, label, args):
        Api.Message("§b命令帮助\n§r模块")
        for key, value in ModuleManager.GetModuleTypes().items():
            Api.Message("§e" + key)
            for module in value:
                Api.Message("§7" + module.name + " - §o" + module.description)
        Api.Message("§b命令")
        for command in commands:
            for name in [command.name] + command.aliases:
                Api.Message("§7" + name + " - §o" + command.description)
        return True