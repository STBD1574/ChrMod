# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
import ChrMod.Api as Api
import math
from ChrMod.Module.ModuleManager import Module
from ChrMod.Module.ModuleManager import ModuleType
from ChrMod.Client import instance as Client

class Blink(Module):
    def __init__(self):
        Module.__init__(self, "Blink", "穿墙。", ModuleType.MOVEMENT, False, None, 0, "")
        self.Game = clientApi.GetEngineCompFactory().CreateGame("")
        self.Timer = None

    def OnEnable(self):
        self.Timer = self.Game.AddRepeatedTimer(0.001, self.Blink_Func)

    def OnDisable(self):
        self.Game.CancelTimer(self.Timer)

    def Blink_Func(self):
        sideMovement, forwardMovement = clientApi.GetEngineCompFactory().CreateActorMotion("").GetInputVector()
        yaw = clientApi.GetEngineCompFactory().CreateCamera(clientApi.GetLevelId()).GetCameraRot()[1] + 180
        calcYaw = (yaw + 90) * (math.pi / 180)
        c, s = math.cos(calcYaw), math.sin(calcYaw)
        moveX, moveY = forwardMovement * c - -sideMovement * s, forwardMovement * s + -sideMovement * c
        x, y, z = clientApi.GetEngineCompFactory().CreatePos(clientApi.GetLocalPlayerId()).GetPos()
        Api.Teleport((x + moveX * 0.5, y + (-0.5 if clientApi.GetEngineCompFactory().CreatePlayer(clientApi.GetLocalPlayerId()).isSneaking() else 0.8 if Client.mJump else 0), z + moveY * 0.5))