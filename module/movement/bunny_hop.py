# -*- coding: utf-8 -*-

import math
from ..module import Module, Category
from ..setting import SettingEntry, ValueType
from ...api import client, localplayer, entity

class BunnyHop(Module):
    def __init__(self):
        Module.__init__(self, 'BunnyHop', '像兔子一样跳。', Category.MOVEMENT, None)

        self.localPlayerId = -1
        self.speed = 1
        self.timer = None

        self.RegisterSetting(SettingEntry('Speed', ValueType.FLOAT, 1, 0, 10))

    def OnEnable(self):
        self.localPlayerId = client.GetLocalPlayerId()
        self.timer = client.AddRepeatedTimer(0.001, self.BunnyHop_Func)

    def OnDisable(self):
        client.CancelTimer(self.timer)

    def BunnyHop_Func(self):
        forwardMovement, sideMovement = client.GetInputVector()
        if sideMovement == 0 and forwardMovement == 0:
            return

        calcYaw = (180 - localplayer.GetCameraRotation()[1]) * (math.pi / 180)
        c, s = math.cos(calcYaw), math.sin(calcYaw)

        moveX = forwardMovement * c - sideMovement * s
        moveY = forwardMovement * s + sideMovement * c

        entity.SetMotion(self.localPlayerId, (moveX * self.speed, 0.42 if entity.IsEntityOnGround(self.localPlayerId) else entity.GetMotion(self.localPlayerId)[1] - 0.09, moveY * self.speed))

    def OnSettingUpdate(self, entry):  # type: (SettingEntry) -> None
        Module.OnSettingUpdate(self, entry)
        
        if entry.name == 'Speed':
            self.speed = entry.value