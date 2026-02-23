# -*- coding: utf-8 -*-
from ChrMod.Command.CommandManager import Command
import ChrMod.Config as ChrConfig
import ChrMod.Module.ModuleManager as ModuleManager
import ChrMod.Api as Api

class Config(Command):
    def __init__(self):
        Command.__init__(self, "config", "配置管理器。", ".config <save/load> <configFile>。", [])

    def Execute(self, label, args):
        if len(args) > 1:
            if args[0] == "save":
                ChrConfig.SaveConfig(args[1], False)
                Api.Message("§cC§eh§ar§bMod §7>> §r保存配置 " + args[1] + " 成功!")
            elif args[0] == "load":
                for module in ModuleManager.modules:
                    ModuleManager.ChangeModuleState(module, False, { }, False)
                Api.Message("§cC§eh§ar§bMod §7>> §r加载配置 " + args[1] + ("成功" if ChrConfig.LoadConfig(args[1]) else "失败") + "!")
            else:
                return False
        else:
            return False
        return True