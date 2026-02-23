# -*- coding: utf-8 -*-

from ..module import Module, Category, KeyBoardType
from ...api import modapi, localplayer, client, entity

class ClickTP(Module):
    def __init__(self):
        Module.__init__(self, 'ClickTP', '点击传送。', Category.MOVEMENT, KeyBoardType.KEY_END)

    def OnEnable(self):
        modapi.ListenForEngineClient('RightClickBeforeClientEvent', self, self.OnEvent, 10, True)
        modapi.ListenForEngineClient('HoldBeforeClientEvent', self, self.OnEvent, 10, True)

    def OnDisable(self):
        modapi.UnListenForEngineClient('RightClickBeforeClientEvent', self, self.OnEvent, 10, True)
        modapi.UnListenForEngineClient('HoldBeforeClientEvent', self, self.OnEvent, 10, True)


    def OnEvent(self, args):
        dict = localplayer.PickFacing()
        if dict['type'] == 'Block':
            x = (dict['x'] + 1 if dict['face'] == 5 else dict['x'] - 1 if dict['face'] == 4 else dict['x']) + 0.5
            y = dict['y'] + 3 if dict['face'] == 1 else dict['y'] if dict['face'] == 0 else dict['y'] + 2
            z = (dict['z'] + 1 if dict['face'] == 3 else dict['z'] - 1 if dict['face'] == 2 else dict['z']) + 0.5
            localplayer.SetPosition((x, y, z))
            client.DisplayClientMessage('§aTeleport to §7x: ' + str(x) + ' y: ' + str(y) + ' z: ' + str(z))
        elif dict['type'] == 'Entity':
            x, y, z = entity.GetPosition(dict['entityId'])
            localplayer.SetPosition((x, y + 2, z))
            client.DisplayClientMessage('§aTeleport to §7' + entity.GetName(dict['entityId']))