# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
from ChrMod.Module.ModuleManager import Module
from ChrMod.Module.ModuleManager import ModuleType

class ShowHealth(Module):
    def __init__(self):
        Module.__init__(self, "ShowHealth", "显血。", ModuleType.VISUAL, False, None)
        self.Game = clientApi.GetEngineCompFactory().CreateGame("")

    def OnEnable(self):
        self.Game.ShowHealthBar(True)

    def OnDisable(self):
        self.Game.ShowHealthBar(False)

