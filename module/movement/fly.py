# -*- coding: utf-8 -*-

import math
from ...module.module import Module, Category, KeyBoardType
from ...module.setting import SettingEntry, ValueType
from ...api import client, localplayer, modapi, entity

class Fly(Module):
    def __init__(self):
        Module.__init__(self, 'Fly', '飞行。', Category.MOVEMENT, KeyBoardType.KEY_HOME)

        self.timer = None
        self.speed = 1.0
        self.isJump = False
        self.localPlayerId = -1

        self.RegisterSetting(SettingEntry('Speed', ValueType.FLOAT, 1, 0, 10))

    def OnEnable(self):
        self.localPlayerId = client.GetLocalPlayerId()
        self.timer = client.AddRepeatedTimer(0.001, self.Fly_Func)

        modapi.ListenForEngineClient('ClientJumpButtonPressDownEvent', self, self.ClientJumpButtonEvent, 10)
        modapi.ListenForEngineClient('ClientJumpButtonReleaseEvent', self, self.ClientJumpButtonEvent, 10)

    def OnDisable(self):
        client.CancelTimer(self.timer)

        modapi.UnListenForEngineClient('ClientJumpButtonPressDownEvent', self, self.ClientJumpButtonEvent, 10)
        modapi.UnListenForEngineClient('ClientJumpButtonReleaseEvent', self, self.ClientJumpButtonEvent, 10)

    def ClientJumpButtonEvent(self, args):
        self.isJump = args != { }

    def Fly_Func(self):
        forwardMovement, sideMovement = client.GetInputVector()
        ym = -1 * self.speed if localplayer.IsSneaking(self.localPlayerId) else (1 * self.speed if self.isJump else 0)

        calcYaw = (-localplayer.GetCameraRotation()[1] + 180) * (math.pi / 180)
        c, s = math.cos(calcYaw), math.sin(calcYaw)

        moveX = forwardMovement * c - sideMovement * s
        moveY = forwardMovement * s + sideMovement * c

        entity.SetMotion(self.localPlayerId, (moveX * self.speed, ym, moveY * self.speed))

    def OnSettingUpdate(self, entry):  # type: (SettingEntry) -> None
        Module.OnSettingUpdate(self, entry)
        
        if entry.name == 'Speed':
            self.speed = entry.value
    