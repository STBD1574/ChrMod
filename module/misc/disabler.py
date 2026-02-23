# -*- coding: utf-8 -*-

from ..module import Module, Category
from ...api import modapi, client

class Disabler(Module):
    def __init__(self):
        Module.__init__(self, "Disabler", "绕过某些反作弊的检测。", Category.MISC, None)

    def OnEnable(self):
        pass

    def OnDisable(self):
        pass
