# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
from ChrMod.Module.ModuleManager import Module
from ChrMod.Module.ModuleManager import ModuleType
import ChrMod.Api as Api
import random

class Invisibility(Module):
    def __init__(self):
        Module.__init__(self, "Invisibility", "让玩家隐身。", ModuleType.MISC, False, None, 2)
        self.Game = clientApi.GetEngineCompFactory().CreateGame("")
        self.Camera = clientApi.GetEngineCompFactory().CreateCamera("")
        self.Timer = None
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0

    def OnEnable(self):
        #self.Timer = self.Game.AddRepeatedTimer(0.001, self.Invisibility_Func)
        return True

    def OnDisable(self):
        #self.Game.CancelTimer(self.Timer)
        #self.Camera.SetCameraAnchor((0, 0, 0))
        return True

    def Invisibility_Func(self):
        Api.Teleport(self.x, self.y, self.z)
        self.x, self.y, self.z = clientApi.GetEngineCompFactory().CreatePos(clientApi.GetLocalPlayerId()).GetPos()
        value = random.randint(10, 100)
        self.Camera.SetCameraAnchor((0, value - self.y, 0))
        Api.Teleport(self.x, self.y - value, self.z)
