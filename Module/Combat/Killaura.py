# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
from ChrMod.Module.ModuleManager import Module, ModuleType
from mod.common.minecraftEnum import KeyBoardType
from ChrMod.Client import instance as Client
import math

class Killaura(Module):
    def __init__(self):
        Module.__init__(self, "Killaura", "杀戮光环。", ModuleType.COMBAT, False, KeyBoardType.KEY_INSERT)
        self.Game = clientApi.GetEngineCompFactory().CreateGame("")
        self.Camera = clientApi.GetEngineCompFactory().CreateCamera("")
        self.Motion = clientApi.GetEngineCompFactory().CreateActorMotion(clientApi.GetLocalPlayerId())
        self.Rotation = clientApi.GetEngineCompFactory().CreateRot(clientApi.GetLocalPlayerId())
        self.Timer = None

    def OnEnable(self):
        self.Timer = self.Game.AddRepeatedTimer(0.001, self.Killaura_Func)
        self.Camera.DepartCamera()

    def OnDisable(self):
        self.Game.CancelTimer(self.Timer)
        self.Camera.UnDepartCamera()

    def Killaura_Func(self):
        if Client.mCurrentEntity == 0: #无实体
            return
        minPos = clientApi.GetEngineCompFactory().CreatePos(Client.mCurrentEntity).GetPos()
        self.Rotation.SetPlayerLookAtPos(minPos, 150, 150, True)      

