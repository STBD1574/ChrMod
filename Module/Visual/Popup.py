# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
from ChrMod.Module.ModuleManager import Module
from ChrMod.Module.ModuleManager import ModuleType
import ChrMod.Api as Api
from ChrMod.Client import instance as Client

class Popup(Module):
    def __init__(self):
        Module.__init__(self, "Popup", "在底部显示信息。", ModuleType.VISUAL, False, None)
        self.Game = clientApi.GetEngineCompFactory().CreateGame("")
        self.Type = 0 #0: hytmod, 1: oldchr, 2: message

    def Update(self):
        if Client.mTick % 3 == 0 and self.open:
            if self.Type == 0:
                Api.TipMessage("InputMode: " + str(clientApi.GetEngineCompFactory().CreatePlayerView(clientApi.GetLevelId()).GetToggleOption("INPUT_MODE") + 1) + " Platform: " + str(clientApi.GetPlatform()) + " FPS: " + str(int(self.Game.GetFps())))
            elif self.Type == 1:
                Motion = clientApi.GetEngineCompFactory().CreateActorMotion(clientApi.GetLocalPlayerId()).GetMotion()
                bps = (Motion[0] ** 2 + Motion[2] ** 2) ** 0.5
                Api.TipMessage("§l§cC§eh§ar§bMod§7 >> §r§bSpeed： " + str(round((bps - int(bps)) * 10, 1)) + " block/s §r| §gFPS： " + str(int(self.Game.GetFps())))

    def Execute(self, label, args):
        if args[0] == "0" or args[0] == "h":
            self.Type = 0
        elif args[0] == "1" or args[0] == "c":
            self.Type = 1
