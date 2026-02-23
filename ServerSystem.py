# -*- coding: utf-8 -*-

import mod.server.extraServerApi as serverApi
import Listener
ServerSystem = serverApi.GetServerSystemCls()
ListenerFactory = Listener.ListenerFactory()
EngineListener = ListenerFactory.CreateListener(namespace = "Minecraft", systemName = "Engine")
Listen = ListenerFactory.CreateListenerProxy()

def sendMessage(playerId, msg, color=''):
    serverApi.GetEngineCompFactory().CreateMsg(serverApi.GetLevelId()).NotifyOneMessage(playerId, msg, color)

class Main(ServerSystem):
    def __init__(self, namespace, systemName):
        ServerSystem.__init__(self, namespace, systemName)

    @EngineListener("ServerChatEvent")
    def OnPlayerChat(self, args):
        sendMessage(args["playerId"], "msg: " + args["message"])
        pass

