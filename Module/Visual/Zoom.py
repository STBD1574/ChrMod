# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
from ChrMod.Module.ModuleManager import Module
from ChrMod.Module.ModuleManager import ModuleType
from mod.common.minecraftEnum import KeyBoardType
import ChrMod.Api as Api
import time

class Zoom(Module):
    def __init__(self):
        Module.__init__(self, "Zoom", "放大。", ModuleType.VISUAL, False, KeyBoardType.KEY_C, 1)
        self.mCamera = clientApi.GetEngineCompFactory().CreateCamera("")
        self.mFov = 0

    def OnEnable(self):
        if self.mCamera.GetFov() != 30.0:
            self.mFov = self.mCamera.GetFov()
            self.mCamera.SetFov(30.0)

    def OnDisable(self):
        self.mCamera.SetFov(self.mFov)