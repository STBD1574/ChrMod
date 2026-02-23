# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
from ChrMod.Module.ModuleManager import Module
from ChrMod.Module.ModuleManager import ModuleType
import ChrMod.Api as Api

class Reach(Module):
    def __init__(self):
        Module.__init__(self, "Reach", "长臂猿。", ModuleType.COMBAT, False, None)
        self.mPlayer = clientApi.GetEngineCompFactory().CreatePlayer("")
        self.mRange = self.mPlayer.GetPickRange()
        self.mRange2 = 1000


    def OnEnable(self):
        self.mPlayer.SetPickRange(self.mRange2)

    def OnDisable(self):
        self.mPlayer.SetPickRange(self.mRange)

    def Execute(self, label, args):
        try:
            self.mRange2 = float(args[0])
            Api.Message("§cC§eh§ar§bMod §7>> §r修改成功!")
        except:
            return False