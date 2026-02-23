# -*- coding: utf-8 -*-

from ..module import Module, Category, KeyBoardType
from ...api import ui

class ClickGui(Module):
    def __init__(self):
        Module.__init__(self, "ClickGui", "点击式UI。", Category.VISUAL, KeyBoardType.KEY_GRAVE)

        self.screenNode = None
        
    def OnEnable(self):
        self.screenNode = ui.PushScreen('chrmod', 'ClickGUI', {'background': 'textures/ui/Black.png', 'module': self})
    
    def OnDisable(self):
        if self.screenNode:
            self.screenNode.CloseButtonClick(None)