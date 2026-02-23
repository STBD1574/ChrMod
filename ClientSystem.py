# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi
import Listener
ClientSystem = clientApi.GetClientSystemCls()
ListenerFactory = Listener.ListenerFactory()
EngineListener = ListenerFactory.CreateListener(namespace = "Minecraft", systemName = "Engine")
Listen = ListenerFactory.CreateListenerProxy()

#封装常用函数，本地玩家id永远是-2
def sendMessage(text):
    clientApi.GetEngineCompFactory().CreateTextNotifyClient(-2).SetLeftCornerNotify(text)

@Listen()
class Main(ClientSystem):
    def __init__(self, namespace, systemName):
        ClientSystem.__init__(self, namespace, systemName)

        self.gameComp = clientApi.GetEngineCompFactory().CreateGame(-2)
        self.cameraComp = clientApi.GetEngineCompFactory().CreateCamera(-2)

        self.sprint = True
        self.bind = False
        self.entity = None
        self.gameComp.AddRepeatedTimer(1, self.ShowInfo)

        sendMessage("§cC§eh§ar§bMod§7 >> §r加载完毕!")

        #playerPos = clientApi.GetEngineCompFactory().CreatePos(-2).GetPos()
        #entities = self.gameComp.GetEntityInArea(-2, (playerPos[0] - 10,playerPos[1] - 10,playerPos[2] - 10), (playerPos[0] + 10,playerPos[1] + 10,playerPos[2] + 10))
    @EngineListener("OnScriptTickClient")
    def ScriptTick(self):
        entity = self.cameraComp.GetChosenEntity()
        if (entity != None and self.bind):
            self.cameraComp.SetCameraBindActorId(entity)
        else:
            self.cameraComp.ResetCameraBindActorId()


    @EngineListener("OnKeyPressInGame")
    def OnPressKey(self, args):
        if args["isDown"] == "1": #按下按键
            #自动疾跑
            if args["key"] == "73":
                if self.sprint:
                    self.gameComp.SetPopupNotice("§7使用I键开关自动疾跑", "§c自动疾跑已关闭")
                    self.sprint = False
                else:
                    self.gameComp.SetPopupNotice("§7使用I键开关自动疾跑", "§a自动疾跑已开启")
                    self.sprint = True
            #自动疾跑 and FreeCam
            if args["key"] == "87" and self.sprint:
                clientApi.GetEngineCompFactory().CreateActorMotion(-2).BeginSprinting()
            #放大
            if args["key"] == "67":
                self.fov = self.cameraComp.GetFov()
                self.cameraComp.SetFov(30.0)
                self.gameComp.SetTipMessage("§rFov: 30.0")
            #FreeCam
            if args["key"] == "88":
                if self.bind:
                    sendMessage("§cC§eh§ar§bMod§7 >> §rBind Disabled")
                    self.bind = False
                else:
                    sendMessage("§cC§eh§ar§bMod§7 >> §rBind Enabled")
                    self.bind = True
        
        if args["isDown"] == "0": #抬起按键
            #自动疾跑
            if args["key"] == "87" and self.sprint:
                clientApi.GetEngineCompFactory().CreateActorMotion(-2).EndSprinting()
            #放大
            if args["key"] == "67":
                self.cameraComp.SetFov(self.fov)
                self.gameComp.SetTipMessage("§rFov: " + str(self.fov))

    def ShowInfo(self):
        self.gameComp.SetTipMessage("FPS: " + self.gameComp.GetFps())
