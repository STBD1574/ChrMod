# -*- coding: utf-8 -*-

from mod.common.mod import Mod
import mod.client.extraClientApi as clientApi
import mod.server.extraServerApi as serverApi
import modConfig

@Mod.Binding(name = modConfig.modName, version = "0.0.1")
class Script(object):

    def __init__(self):
        pass

    @Mod.InitServer()
    def ScriptServerInit(self):
        #client帮忙加载了( •̀ ω •́ )y
        pass

    @Mod.DestroyServer()
    def ScriptServerDestroy(self):
        pass

    @Mod.InitClient()
    def ScriptClientInit(self):
        clientApi.RegisterSystem(modConfig.modName, modConfig.clientSysName, modConfig.clientClsPath)
        serverApi.RegisterSystem(modConfig.modName, modConfig.serverSysName, modConfig.serverClsPath)

    @Mod.DestroyClient()
    def ScriptClientDestroy(self):
        pass
