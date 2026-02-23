# -*- coding: utf-8 -*-

from ..module import Module, Category
import mod.client.extraClientApi as clientApi

class ESP(Module):
    def __init__(self):
        Module.__init__(self, "ESP", "显示玩家的碰撞箱。", Category.VISUAL, None)

    def OnEnable(self):
        frameAniControlComp = clientApi.GetEngineCompFactory().CreateFrameAniControl('')
        frameAniControlComp.SetMixColor((1, 0, 0, 0.12))
        frameAniControlComp.SetDeepTest(False)
        frameAniControlComp.Play()