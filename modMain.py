# -*- coding: utf-8 -*-

from mod.common.mod import Mod
import mod.server.extraServerApi as serverApi
import mod.client.extraClientApi as clientApi
import modConfig

@Mod.Binding(name=modConfig.modName, version="0.0.1")
class Script(object):

    def __init__(self):
        pass

    @Mod.InitServer()
    def ScriptServerInit(self):
        serverApi.RegisterSystem(modConfig.modName, modConfig.serverSysName, modConfig.serverClsPath)

    @Mod.InitClient()
    def ScriptClientInit(self):
        clientApi.RegisterSystem(modConfig.modName, modConfig.clientSysName, modConfig.clientClsPath)

