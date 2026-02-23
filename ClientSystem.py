# -*- coding: utf-8 -*-
# 反编译你妈啊, 源码不会自己要吗?
import mod.client.extraClientApi as clientApi
import Listener
ClientSystem = clientApi.GetClientSystemCls()
ListenerFactory = Listener.ListenerFactory()
EngineListener = ListenerFactory.CreateListener(namespace = "Minecraft", systemName = "Engine")
Listen = ListenerFactory.CreateListenerProxy()

#封装常用函数
def sendMessage(text):
    return clientApi.GetEngineCompFactory().CreateTextNotifyClient(clientApi.GetLocalPlayerId()).SetLeftCornerNotify(text)

#Module类
class Module(object):
    def __init__(self, name, isopen, key="-1", function=None):
        #type: (str, bool, str, function) -> Module
        '''
        function有一个参数: moudle
        '''
        self.name = name
        self.isopen = isopen
        self.key = key
        self.function = function

@Listen()
class Main(ClientSystem):
    def __init__(self, namespace, systemName):
        ClientSystem.__init__(self, namespace, systemName)

        self.gameComp = clientApi.GetEngineCompFactory().CreateGame(clientApi.GetLocalPlayerId())
        self.cameraComp = clientApi.GetEngineCompFactory().CreateCamera(clientApi.GetLocalPlayerId())
        self.motionComp = clientApi.GetEngineCompFactory().CreateActorMotion(clientApi.GetLocalPlayerId())

        self.downkey = dict()
        self.modules = [
            Module("Bind", False, "88", self.Bind), #Key_X
            Module("HighJump", False, "77", self.HighJump), #Key_M
            Module("Flight", False, "75"), #Key_K
            Module("Aimbot", False, "76") #Key_L
        ]

        self.disable = False
        self.tick = 0
        self.sprint = True
        self.entity = None
        self.entities = None

        sendMessage("§cC§eh§ar§bMod§7 >> §r加载完毕!")
        sendMessage("§cC§eh§ar§bMod§7 >> §r欢迎使用ChrMod, 版本V1.1")
        sendMessage("§cC§eh§ar§bMod§7 >> §r==== 快捷键 ====")
        sendMessage("§cC§eh§ar§bMod§7 >> §rI: 自动疾跑 C:放大")
        sendMessage("§cC§eh§ar§bMod§7 >> §rX: 附身 M: 高跳")
        sendMessage("§cC§eh§ar§bMod§7 >> §rK: 飞行 L: 自瞄")
        sendMessage("§cC§eh§ar§bMod§7 >> §r===============")
        sendMessage("§cC§eh§ar§bMod§7 >> §rPlatform: " + str(clientApi.GetPlatform()))
        sendMessage("§cC§eh§ar§bMod§7 >> §rUid: " + str(clientApi.GetEngineCompFactory().CreatePlayer(clientApi.GetLocalPlayerId()).getUid()))
        sendMessage("§cC§eh§ar§bMod§7 >> §rIP: " + clientApi.GetIP())
        
    @EngineListener("OnScriptTickClient")
    def ScriptTick(self):
        if self.disable:
            return
        self.entity = self.cameraComp.GetChosenEntity()
        if self.tick % 3 == 0:
            playerMotion = self.motionComp.GetMotion()
            self.gameComp.SetTipMessage("§l§cC§eh§ar§bMod§7 >> §r§aMotion： " + str(playerMotion[0]) + " | " + str(playerMotion[1]) + " | " + str(playerMotion[2]))
            if self.modules[2].isopen: #Flight
                self.Flight_Func()
            if self.modules[3].isopen: #Flight
                self.AutoAiming_Func()
        self.tick += 1

    @EngineListener("OnKeyPressInGame")
    def OnPressKey(self, args):
        #args["screenName"]
        if self.disable:
            return
        if args["isDown"] == "1": #按下按键
            self.downkey[args["key"]] = True
            #自动疾跑: I
            if args["key"] == "73":
                if self.sprint:
                    self.gameComp.SetPopupNotice("§7使用I键开关自动疾跑", "§c自动疾跑已关闭")
                    self.sprint = False
                else:
                    self.gameComp.SetPopupNotice("§7使用I键开关自动疾跑", "§a自动疾跑已开启")
                    self.sprint = True
            #自动疾跑: W
            if args["key"] == "87" and self.sprint:
                self.motionComp.BeginSprinting()
            #放大: C
            if args["key"] == "67":
                self.fov = self.cameraComp.GetFov()
                self.cameraComp.SetFov(30.0)
                self.gameComp.SetTipMessage("§rFov: 30.0")
            #Modules
            for module in self.modules:
                if args["key"] == module.key:
                    if module.isopen:
                        sendMessage("§cC§eh§ar§bMod§7 >> §r" + module.name + " Disabled")
                        module.isopen = False
                    else:
                        sendMessage("§cC§eh§ar§bMod§7 >> §r" + module.name + " Enabled")
                        module.isopen = True
                    if module.function != None: 
                        module.function(module)

        if args["isDown"] == "0": #抬起按键
            self.downkey[args["key"]] = False
            #自动疾跑: W
            if args["key"] == "87" and self.sprint:
                self.motionComp.EndSprinting()
            #放大: C
            if args["key"] == "67":
                self.cameraComp.SetFov(self.fov)
                self.gameComp.SetTipMessage("§rFov: " + str(self.fov))

    # ============ Module ============
    def Bind(self, module):
        if module.isopen:
            if self.cameraComp.SetCameraBindActorId(self.entity) == False:
                sendMessage("§cC§eh§ar§bMod§7 >> §r请对准生物后重新开启此功能")   
                module.isopen = False
        else:
            self.cameraComp.ResetCameraBindActorId()

    def HighJump(self, module):
        module.isopen = False
        self.motionComp.SetMotion((0, 1.2, 0))

    def Flight_Func(self):
        yrot, xrot = clientApi.GetEngineCompFactory().CreateRot(clientApi.GetLocalPlayerId()).GetRot()
        flightSpeed = 1
        #if self.downkey["16"] or self.downkey["17"]: #LShift: 16, Ctrl:17
        #    ym = -1 * flightSpeed
        if self.downkey["32"]: #Space: 32
            ym = 1 * flightSpeed
        else:
            ym = 0
        #W: 87, A:65, S:83, D:68
        x, z = 0.0, 0.0
        if self.downkey.get("87", False):
            x, y, z = clientApi.GetDirFromRot((6 , xrot))
        if self.downkey.get("65", False):
            x, y, z = clientApi.GetDirFromRot((6 , xrot - 83.55))
        if self.downkey.get("83", False):
            x, y, z = clientApi.GetDirFromRot((6 , xrot - 180))
        if self.downkey.get("68", False):
            x, y, z = clientApi.GetDirFromRot((6 , xrot + 83.55))
        if self.downkey.get("87", False) and self.downkey.get("65", False):
            x, y, z = clientApi.GetDirFromRot((6 , xrot - 41.755))
        if self.downkey.get("87", False) and self.downkey.get("68", False):
            x, y, z = clientApi.GetDirFromRot((6 , xrot + 41.755))
        if self.downkey.get("83", False) and self.downkey.get("65", False):
            x, y, z = clientApi.GetDirFromRot((6 , xrot + 221.775))
        if self.downkey.get("83", False) and self.downkey.get("68", False):
            x, y, z = clientApi.GetDirFromRot((6 , xrot - 221.775))
        self.motionComp.SetMotion((x * flightSpeed, ym , z * flightSpeed))
        if self.downkey.get("65", False) == False and self.downkey.get("87", False) == False and self.downkey.get("83", False) == False and self.downkey.get("68", False) == False:
            self.motionComp.SetMotion((0, ym, 0))

    def AutoAiming_Func(self):
        minDist = 999
        minPos = ()
        if self.entity != "":
            entity = self.entity
            strid = str(entity)
            strlang= len(strid)
            if strlang > 5 and entity != clientApi.GetLocalPlayerId():
                enemyPos = clientApi.GetEngineCompFactory().CreatePos(entity).GetPos()
                minPos = enemyPos
                clientApi.GetEngineCompFactory().CreateRot(clientApi.GetLocalPlayerId()).SetPlayerLookAtPos(minPos, 999, 999, True)	



