# -*- coding: utf-8 -*-

import math
from ..module import Module, Category
from ..setting import SettingEntry, ValueType
from ...api import client, localplayer, modapi, entity

class BoatFly(Module):
    def __init__(self):
        Module.__init__(self, 'BoatFly', '船飞。', Category.MOVEMENT, None)

        self.localPlayerId = 0
        self.timer = 0
        self.speed = 1

        self.RegisterSetting(SettingEntry('Speed', ValueType.FLOAT, 1, 0, 10))

    def OnEnable(self):
        self.localPlayerId = client.GetLocalPlayerId()
        self.timer = client.AddRepeatedTimer(0.001, self.BoatFly_Func)

        modapi.ListenForEngineClient('StartRidingClientEvent', self, self.StartRidingClientEvent, 10)
        modapi.ListenForEngineClient('EntityStopRidingEvent', self, self.EntityStopRidingEvent, 10)
        modapi.ListenForEngineClient('OnKeyPressInGame', self, self.OnKeyPressInGame, 10)

    def OnDisable(self):
        client.CancelTimer(self.timer)

        modapi.UnListenForEngineClient('StartRidingClientEvent', self, self.StartRidingClientEvent, 10)
        modapi.UnListenForEngineClient('EntityStopRidingEvent', self, self.EntityStopRidingEvent, 10)
        modapi.UnListenForEngineClient('OnKeyPressInGame', self, self.OnKeyPressInGame, 10)
    
    def StartRidingClientEvent(self, args):
        if  args['actorId'] == self.localPlayerId and entity.GetType(args['victimId']) == 'minecraft:boat':
            localplayer.DepartCamera()

    def EntityStopRidingEvent(self, args):
        if args['id'] == self.localPlayerId:
            localplayer.UnDepartCamera()

    def OnKeyPressInGame(self, args):
        if args['screenName'] != 'hud_screen':
            return
        
        self.isAscend = args['key'] == '20' and args['isDown'] == '1'
        self.isDescend = args['key'] == '17' and args['isDown'] == '1'

    def BoatFly_Func(self):
        riderId = entity.GetEntityRider(self.localPlayerId)
        if riderId == -1 or entity.GetType(riderId) != 'minecraft:boat':
            return
        
        forwardMovement, sideMovement = client.GetInputVector()
        ym = -1 * self.speed if self.isDescend else (1 * self.speed if self.isAscend else 0)

        calcYaw = (-localplayer.GetCameraRotation()[1] + 180) * (math.pi / 180)
        c, s = math.cos(calcYaw), math.sin(calcYaw)

        moveX = forwardMovement * c - sideMovement * s
        moveY = forwardMovement * s + sideMovement * c

        entity.SetMotion(riderId, (moveX * self.speed, ym, moveY * self.speed))

    def OnSettingUpdate(self, entry):  # type: (SettingEntry) -> None
        Module.OnSettingUpdate(self, entry)
        
        if entry.name == 'Speed':
            self.speed = entry.value
    