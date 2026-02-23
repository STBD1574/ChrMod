# -*- coding: utf-8 -*-

from ...module.module import Module, Category
from ...api import modapi, entity, client, localplayer, math

class Respawn(Module):
    def __init__(self):
        Module.__init__(self, 'Respawn', '原地复活', Category.MOVEMENT, None)

        self.position = None

    def OnEnable(self):
        modapi.ListenForEngineClient('PushScreenEvent', self, self.PushScreenEvent, 10)
        modapi.ListenForEngineClient('PopScreenEvent', self, self.PopScreenEvent, 10)

    def OnDisable(self):
        modapi.UnListenForEngineClient('PushScreenEvent', self, self.PushScreenEvent, 10)
        modapi.UnListenForEngineClient('PopScreenEvent', self, self.PopScreenEvent, 10)

    def PushScreenEvent(self, args):
        if args['screenName'] == 'death_screen':
            self.position = entity.GetPosition(client.GetLocalPlayerId())
            self.dimension = client.GetCurrentDimension()
            client.DisplayClientMessage('§cC§eh§ar§bMod §7>§r Death coordinates X: {} Y: {} Z: {}'.format(*(math.SetPrecision(p, 2) for p in self.position)))

    def PopScreenEvent(self, args):
        if args['screenName'] == 'death_screen':
            if self.position and self.dimension == client.GetCurrentDimension():
                localplayer.SetPosition(self.position)
            self.position = None