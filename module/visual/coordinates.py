# -*- coding: utf-8 -*-
# author Eison
# 2024/08/01

from ...module.module import Module, Category
from ...api import client, modapi, entity, math

class Coordinates(Module):
    def __init__(self):
        Module.__init__(self, "Coordinates", "显示坐标。", Category.VISUAL, None)

    def OnEnable(self):
        modapi.ListenForEngineClient('OnScriptTickClient', self, self.OnScriptTickClient, 10)

    def OnDisable(self):
        modapi.UnListenForEngineClient('OnScriptTickClient', self, self.OnScriptTickClient, 10)

    def OnScriptTickClient(self):
        position = tuple(math.SetPrecision(p, 2) for p in entity.GetPosition(client.GetLocalPlayerId()))

        client.DisplayMessage(4, '坐标: {} {} {}'.format(*position) + ('\n主世界: {} {} {}'.format(math.SetPrecision(position[0] / 8, 2), position[1], math.SetPrecision(position[2] / 8, 2)) if client.GetCurrentDimension() == 1 else ''), '', '')
        