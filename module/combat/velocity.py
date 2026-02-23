# -*- coding: utf-8 -*-

from ...module.module import Module, Category
from ...api import client, entity, modapi

class Velocity(Module):
    def __init__(self):
        Module.__init__(self, "Velocity", "无击退。", Category.COMBAT, None)

        self.localplayer = -2
        self.motion = None
        
    def OnEnable(self):
        self.localplayer = client.GetLocalPlayerId()

        modapi.ListenForEngineClient('OnScriptTickClient', self, self.OnScriptTickClient, 10)
        modapi.ListenForEngineClient('HealthChangeClientEvent', self, self.HealthChangeClientEvent, 10)

    def OnDisable(self):
        modapi.UnListenForEngineClient('OnScriptTickClient', self, self.OnScriptTickClient, 10)
        modapi.UnListenForEngineClient('HealthChangeClientEvent', self, self.HealthChangeClientEvent, 10)

    def OnScriptTickClient(self):
        self.motion = entity.GetMotion(self.localplayer)

    def HealthChangeClientEvent(self, args):
        if args['entityId'] != self.localplayer or self.motion is None or args['to'] <= 0:
            return
        
        motion = entity.GetMotion(self.localplayer)
        if motion is self.motion:
            return

        entity.SetMotion(self.localplayer, ((motion[0] - self.motion[0]) * 0.496, (motion[1] - self.motion[1]) * 0.496, (motion[2] - self.motion[2]) * 0.496))