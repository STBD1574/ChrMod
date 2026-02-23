# -*- coding: utf-8 -*-

from ..module import Module, Category
from ...api import modapi, ui, client

class HudTip(Module):
    def __init__(self):
        Module.__init__(self, 'HudTip', '显示Hud提示（右上角的那个）。', Category.VISUAL, None)

        self.screenNode = None
        
    def OnEnable(self):
        self.screenNode = ui.GetUI('chrmod', 'HudGUI')

        modapi.ListenForEngineClient('OnScriptTickClient', self, self.OnScriptTickClient, 10)

    def OnDisable(self):
        modapi.UnListenForEngineClient('OnScriptTickClient', self, self.OnScriptTickClient, 10)

    def OnScriptTickClient(self):
        self.screenNode.SetTip('§cC§eh§ar§bMod §7| §fPlatform: {} InputMode: {} FPS: {}'.format(modapi.GetPlatform(), modapi.GetInputMode(), int(client.GetFPS())), False)