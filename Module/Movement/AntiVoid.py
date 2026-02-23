# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
from ChrMod.Module.ModuleManager import Module
from ChrMod.Module.ModuleManager import ModuleType
import ChrMod.Api as Api

class AntiVoid(Module):
    def __init__(self):
        Module.__init__(self, "AntiVoid", "虚空自动拉回。", ModuleType.MOVEMENT, False, None)
        self.mGame = clientApi.GetEngineCompFactory().CreateGame("")
        self.mTimer = None
        self.mSafePos = ()

    def OnEnable(self):
        self.mTimer = self.mGame.AddRepeatedTimer(0.25, self.AntiVoid_Func)

    def OnDisable(self):
        self.mGame.CancelTimer(self.mTimer)

    def Update(self):
        localPos = [int(i) for i in Api.Entity.GetPosition(clientApi.GetLocalPlayerId())]
        if "air" not in clientApi.GetEngineCompFactory().CreateBlockInfo(clientApi.GetLevelId()).GetBlock((localPos[0], localPos[1] - 1, localPos[2]))[0]:#安全
            self.mSafePos = localPos

    def AntiVoid_Func(self):
        if not clientApi.GetEngineCompFactory().CreateAttr(clientApi.GetLocalPlayerId()).isEntityOnGround() and abs(self.mSafePos[1] - Api.Entity.GetPosition(clientApi.GetLocalPlayerId())[1]) > 5:
            Api.Teleport(self.mSafePos)