# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
from ChrMod.Module.ModuleManager import Module
from ChrMod.Module.ModuleManager import ModuleType
from mod.common.minecraftEnum import KeyBoardType
import ChrMod.Api as Api
from ChrMod.Client import instance as Client
import math

class Fly(Module):
    def __init__(self):
        Module.__init__(self, "Fly", "飞行。", ModuleType.MOVEMENT, False, KeyBoardType.KEY_HOME, 0, ".fly <mode: 0(Motion), 1(BunnyHop)>")
        self.Game = clientApi.GetEngineCompFactory().CreateGame("")
        self.Speed = 1
        self.Type = 0 #0: Motion, 1: BunnyHop
        self.Timer = None

    def OnEnable(self):
        self.Timer = self.Game.AddRepeatedTimer(0.001, self.Fly_Func)

    def OnDisable(self):
        self.Game.CancelTimer(self.Timer)

    def Fly_Func(self):
        Motion = clientApi.GetEngineCompFactory().CreateActorMotion(clientApi.GetLocalPlayerId())
        sideMovement, forwardMovement = clientApi.GetEngineCompFactory().CreateActorMotion("").GetInputVector()
        yaw = clientApi.GetEngineCompFactory().CreateCamera(clientApi.GetLevelId()).GetCameraRot()[1] + 180
        ym = -1 * self.Speed if clientApi.GetEngineCompFactory().CreatePlayer(clientApi.GetLocalPlayerId()).isSneaking() else 1 * self.Speed if Client.mJump else 0
        calcYaw = (yaw + 90) * (math.pi / 180)
        c, s = math.cos(calcYaw), math.sin(calcYaw)
        moveX, moveY = forwardMovement * c - -sideMovement * s, forwardMovement * s + -sideMovement * c
        isOnGound = clientApi.GetEngineCompFactory().CreateAttr(clientApi.GetLocalPlayerId()).isEntityOnGround()
        if self.Type == 0: #motion
            Motion.SetMotion((moveX * self.Speed, ym, moveY * self.Speed))
        elif self.Type == 1: #bhop
            if sideMovement != 0 or forwardMovement != 0:
                clientApi.GetEngineCompFactory().CreateActorMotion(clientApi.GetLocalPlayerId()).SetMotion((moveX * 0.5, 0.42 if isOnGound else Motion.GetMotion()[1] - 0.09, moveY * 0.5))

    def Execute(self, label, args):
        try:
            val = int(args[0])
            self.Type = val if val > -1 and val < 2 else self.Type
            Api.Message("§cC§eh§ar§bMod §7>> §r设置成功！")
        except:
            return False
        return True