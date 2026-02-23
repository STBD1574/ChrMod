# -*- coding: utf-8 -*-
from ChrMod.Command.CommandManager import Command
import ChrMod.Api as Api
from mod.common.minecraftEnum import KeyBoardType
import ChrMod.Module.ModuleManager as ModuleManager

class Bind(Command):
    def __init__(self):
        Command.__init__(self, "bind", "绑定模块的快捷键 (使用键代码或键名，设置None为解绑)。", ".bind <module> <key>", [])

    def Execute(self, label, args): #type: (str, list[str]) -> bool
        try:
            for module in ModuleManager.modules:
                if module.name.lower() == args[0].lower():
                    module.key = args[1]
                    for key in dir(KeyBoardType):
                        if key.startswith("KEY_"):
                            print(key[4:].lower())
                            if key[4:].lower() == args[1].lower():
                                module.key = getattr(KeyBoardType, key)
                                break
            Api.Message("§cC§eh§ar§bMod §7>> §r绑定成功!")
        except:
            return False
        return True