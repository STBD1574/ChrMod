# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
from ChrMod.Module.ModuleManager import Module
from ChrMod.Module.ModuleManager import ModuleType
from mod.common.minecraftEnum import KeyBoardType
from ChrMod.Client import instance as Client

class Aimbot(Module):
    def __init__(self):
        Module.__init__(self, "Aimbot", "自动瞄准。", ModuleType.COMBAT, False, KeyBoardType.KEY_PERIOD)
        self.Game = clientApi.GetEngineCompFactory().CreateGame("")
        self.Timer = None

    def OnEnable(self):
        self.Timer = self.Game.AddRepeatedTimer(0.001, self.Aimbot_Func)

    def OnDisable(self):
        self.Game.CancelTimer(self.Timer)

    def Aimbot_Func(self):
        if Client.mCurrentEntity == 0: #无实体
            return
        minPos = clientApi.GetEngineCompFactory().CreatePos(Client.mCurrentEntity).GetPos()
        clientApi.GetEngineCompFactory().CreateRot(clientApi.GetLocalPlayerId()).SetPlayerLookAtPos(minPos, 150, 150, True)