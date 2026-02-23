# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
from ChrMod.Module.ModuleManager import Module
from ChrMod.Module.ModuleManager import ModuleType
from mod.common.minecraftEnum import KeyBoardType
import ChrMod.Api as Api

class Spammer(Module):
    def __init__(self):
        Module.__init__(self, "Spammer", "自动发送消息 （__为空格，/开头发送命令）。", ModuleType.MISC, False, KeyBoardType.KEY_PG_DOWN, 0, ".spammer <text> <delay>")
        self.Game = clientApi.GetEngineCompFactory().CreateGame("")
        self.Timer = None
        self.Delay = 1
        self.Text = "ChrMod V3"

    def OnEnable(self):
        self.Timer = self.Game.AddRepeatedTimer(self.Delay, self.Spammer_Func)

    def OnDisable(self):
        self.Game.CancelTimer(self.Timer)
    
    def Spammer_Func(self):
        if self.Text[0] == "/":
            Api.SendCommand(self.Text[1:])
        else:
            Api.SendChatMsg(self.Text)

    def Execute(self, label, args): #type: (str, list[str]) -> None
        try:
            self.Text = args[0].replace("__", " ")
            self.Delay = float(args[1])
            Api.Message("§cC§eh§ar§bMod §7>> §r设置成功!")
        except:
            return False
        return True
            