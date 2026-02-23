# -*- coding: utf-8 -*-
# 我认为，这个modMain还是有意义的。

from mod.common.mod import Mod
import mod.server.extraServerApi as serverApi

@Mod.Binding(name="ChrMod", version="0.0.1")
class ChrMod(object):

    def __init__(self):
        pass

    @Mod.InitServer()
    def ChrModServerInit(self):
        serverApi.RegisterSystem("ChrMod", "Server", "ChrMod.Server.Main")

    @Mod.DestroyServer()
    def ChrModServerDestroy(self):
        pass

    @Mod.InitClient()
    def ChrModClientInit(self):
        pass

    @Mod.DestroyClient()
    def ChrModClientDestroy(self):
        pass
