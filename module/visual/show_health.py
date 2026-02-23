# -*- coding: utf-8 -*-

from ..module import Module, Category
from ...api import client

class ShowHealth(Module):
    def __init__(self):
        Module.__init__(self, "ShowHealth", "显血。", Category.VISUAL, None)

    def OnEnable(self):
        client.ShowHealthBar(True)

    def OnDisable(self):
        client.ShowHealthBar(False)

