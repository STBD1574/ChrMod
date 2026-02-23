# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
from ChrMod.Module.ModuleManager import Module, ModuleType
from mod.common.minecraftEnum import KeyBoardType
import ChrMod.Api as Api
from ChrMod.uiScript.Gui import Controls

class ClickGui(Module):
    def __init__(self):
        Module.__init__(self, "ClickGui", "点击式UI。", ModuleType.VISUAL, False, KeyBoardType.KEY_GRAVE, 0, "", background="textures/ui/Black.png")
        Api.ListenForEvent("Minecraft", "Engine", "UiInitFinished", self, self.UiInitFinished, 10)
        self.mScreenNode = None

    def UiInitFinished(self, args):
        clientApi.RegisterUI("chrmod", "clickGui", "ChrMod.uiScript.ClickGui.Main", Controls.SCREEN)

    def OnEnable(self):
        self.open = True
        self.mScreenNode = clientApi.PushScreen("chrmod", "clickGui", {"module": self, "background": self.args["background"]})
        return True
    
    def OnDisable(self):
        self.mScreenNode.CloseButtonClick()