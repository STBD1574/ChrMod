# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
from ChrMod.Command.CommandManager import Command
import ChrMod.Api as Api

def SetPlatform(platform):
    clientApi.GetPlatform = lambda : platform

class Platform(Command):
    def __init__(self):
        Command.__init__(self, "platform", "修改ModAPI识别的Platform (0：Windows； 1：IOS； 2：Android； 3：Linux)。", ".platform <platform>")

    def Execute(self, label, args):
        if len(args) > 0:
            try:
                SetPlatform(int(args[0]))
                Api.Message("§cC§eh§ar§bMod §7>> §r修改成功!")
            except:
                return False
        else:
            return False
        return True