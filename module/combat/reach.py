# -*- coding: utf-8 -*-

from ..module import Module, Category
from ..setting import SettingEntry, ValueType
from ...api import localplayer

class Reach(Module):
    def __init__(self):
        Module.__init__(self, 'Reach', '长臂猿。', Category.COMBAT, None)

        self.defaultRange = 5.69999980927
        self.range = 100.0
        self.RegisterSetting(SettingEntry('Range', ValueType.FLOAT, self.range, 1, 100))

    def OnEnable(self):
        localplayer.SetPickRange(self.range)

    def OnDisable(self):
        localplayer.SetPickRange(self.defaultRange)

    def OnSettingUpdate(self, entry): # type: (SettingEntry) -> None
        Module.OnSettingUpdate(self, entry)
        self.range = entry.value
        if self.GetEnabled():
            localplayer.SetPickRange(self.range)

    