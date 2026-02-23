# -*- coding: utf-8 -*-

from ..module import Module, Category
from ..setting import SettingEntry, ValueType
from ...api import modapi, entity, client

class HighJump(Module):
    def __init__(self):
        Module.__init__(self, 'HighJump', '高跳。', Category.MOVEMENT, None)

        self.high = 1.2
        self.RegisterSetting(SettingEntry('high', ValueType.FLOAT, self.high, 0, 10))

    def OnEnable(self):
        self.localPlayerId = client.GetLocalPlayerId()

        modapi.ListenForEngineClient('ClientJumpButtonPressDownEvent', self, self.OnEvent, 10)

    def OnDisable(self):
        modapi.UnListenForEngineClient('ClientJumpButtonPressDownEvent', self, self.OnEvent, 10)

    def OnEvent(self, args):
        args['continueJump'] = False
        if entity.IsEntityOnGround(self.localPlayerId):
            x, _, z = entity.GetMotion(self.localPlayerId)
            entity.SetMotion(self.localPlayerId, (x, self.high, z))

    def OnSettingUpdate(self, entry): # type: (SettingEntry) -> None
        Module.OnSettingUpdate(self, entry)
        self.high = entry.value