# -*- coding: utf-8 -*-

import mod.server.extraServerApi as serverApi
ServerSystem = serverApi.GetServerSystemCls()


class Main(ServerSystem):
    def __init__(self, namespace, systemName):
        ServerSystem.__init__(self, namespace, systemName)
        global instance
        instance = self
        self.ListenForEvent("ChrMod", "qwq", "awa", self, self.OnEvent, 10)

    def OnEvent(self, args):
        try:
            playerId = args["__id__"]
        except:
            playerId = None
        print("OnTestEvent: {} {} {}".format(args, type(args), playerId))

    # OnScriptTickServer的回调函数，会在引擎tick的时候调用，1秒30帧（被调用30次）
    def OnTickServer(self):
        """
        Driven by event, One tick way
        """
        pass

    # 这个Update函数是基类的方法，同样会在引擎tick的时候被调用，1秒30帧（被调用30次）
    def Update(self):
        """
        Driven by system manager, Two tick way
        """
        pass

    def Destroy(self):
        pass
