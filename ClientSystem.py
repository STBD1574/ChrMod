# -*- coding: utf-8 -*-
# 反编译你妈啊, 源码不会自己要吗?
import mod.client.extraClientApi as clientApi
import Listener
ClientSystem = clientApi.GetClientSystemCls()
ListenerFactory = Listener.ListenerFactory()
EngineListener = ListenerFactory.CreateListener(namespace = "Minecraft", systemName = "Engine")
Listen = ListenerFactory.CreateListenerProxy()
#Keys = clientApi.GetMinecraftEnum().KeyBoardType

#封装常用函数
def sendMessage(text):
    #type: (str) -> bool
    return clientApi.GetEngineCompFactory().CreateTextNotifyClient(clientApi.GetLocalPlayerId()).SetLeftCornerNotify(text)

#Module类
class Module(object):
    def __init__(self, name, isopen, key="0", function=None, tags=None):
        #type: (str, bool, str, function, any) -> Module
        '''
        function有一个参数: moudle
        '''
        self.name = name
        self.isopen = isopen
        self.key = key
        self.function = function
        self.tags = tags

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
            Module("Aimbot", False, "76"), #Key_L
            Module("Killaura", False, "82"), #Key_R
            Module("Crasher", False, "80"), #Key_P
            Module("Freecam", False, "79", self.Freecam) #Key_O
        ]

        self.version = "1.2"
        self.disable = clientApi.GetModConfigJson("modconfigs/config.json").get("disable", False)
        self.tick = 0
        self.sprint = True
        self.entity = None
        self.entities = None
        self.onGround = False
        self.jump = False

        self.ListenForEvent("ChrApi", "ChrApi", "ClientTick", self, self.ClientTick)

        sendMessage("§cC§eh§ar§bMod§7 >> §r加载完毕!")
        
    def ClientTick(self):
        self.disable = True
        self.UnListenForEvent("ChrApi", "ChrApi", "ClientTick", self, self.ClientTick)

    def CreateUi(self, ui=clientApi.GetScreenNodeCls()):
        base = ui.GetBaseUIControl("")
        ui.CreateChildControl("chrmod.title", "title", base).asLabel().SetText("ChrMod - V" + self.version)
        
    @EngineListener("UiInitFinished")
    def UiInitFinished(self, args):
        sendMessage("§cC§eh§ar§bMod§7 >> §r欢迎使用ChrMod, 版本V" + self.version)
        sendMessage("§cC§eh§ar§bMod§7 >> §r作者: Eison, Chr_Studio")
        sendMessage("§cC§eh§ar§bMod§7 >> §r========== 快捷键 ==========")
        sendMessage("§cC§eh§ar§bMod§7 >> §rI: 自动疾跑 C:放大")
        sendMessage("§cC§eh§ar§bMod§7 >> §rX: 附身    M: 高跳")
        sendMessage("§cC§eh§ar§bMod§7 >> §rK: 飞行    L: 自瞄")
        sendMessage("§cC§eh§ar§bMod§7 >> §rR: 杀戮    P: 崩服")
        sendMessage("§cC§eh§ar§bMod§7 >> §rN: Freecam")
        sendMessage("§cC§eh§ar§bMod§7 >> §r=========================")
        sendMessage("§cC§eh§ar§bMod§7 >> §rPlatform: " + str(clientApi.GetPlatform()))
        sendMessage("§cC§eh§ar§bMod§7 >> §rUid: " + str(clientApi.GetEngineCompFactory().CreatePlayer(clientApi.GetLocalPlayerId()).getUid()))
        sendMessage("§cC§eh§ar§bMod§7 >> §rIP: " + clientApi.GetIP())

        self.CreateUi(clientApi.GetUI("hud", "hud_screen"))

    @EngineListener("OnCommandOutputClientEvent")
    def CommandOutput(self, args):
        if self.disable:
            return
        sendMessage("§cC§eh§ar§bMod§7 >> §rCommand: " + args["command"] + " Output: " + args["message"])

    @EngineListener("ClientJumpButtonPressDownEvent")
    def ClientJumpPress(self, args):
        self.jump = True

    @EngineListener("ClientJumpButtonReleaseEvent")
    def ClientJumpRelease(self, args):
        self.jump = False

    @EngineListener("OnScriptTickClient")
    def ScriptTick(self):
        if self.disable:
            return
        self.onGround = clientApi.GetEngineCompFactory().CreateAttr(clientApi.GetLocalPlayerId()).isEntityOnGround()
        self.entity = self.cameraComp.GetChosenEntity()
        if self.tick % 3 == 0: #0.1 Second
            Motion = self.motionComp.GetMotion()
            bps = (Motion[0] ** 2 + Motion[2] ** 2) ** 0.5
            self.gameComp.SetTipMessage("§l§cC§eh§ar§bMod§7 >> §r§bSpeed： " + str(round((bps - int(bps)) * 10, 1)) + " block/s §r| §gFPS： " + str(int(self.gameComp.GetFps())))
            if self.modules[2].isopen: #Flight
                self.Flight_Func()
            if self.modules[4].isopen: #Killaura
                self.Killaura_Func()
        if self.modules[5].isopen:
            self.Crasher_Func()
        self.tick += 1
    
    @EngineListener("OnKeyPressInGame")
    def OnPressKey(self, args):
        if self.disable or args["screenName"] != "hud_screen":
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

    # ============ Modules ============
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

    def AutoAiming(self, module):
        if module.isopen:
            self.aimbot_timer = self.gameComp.AddTimer(0.001, self.AutoAiming_Func)
        else:
            self.gameComp.CancelTimer(self.aimbot_timer)

    def Freecam(self, module):
        if module.isopen:
            x, y, z = clientApi.GetEngineCompFactory().CreatePos(clientApi.GetLocalPlayerId()).GetPos()
            self.cameraComp.LockCamera((x, y + 2, z), self.cameraComp.GetCameraRot())

    # ============ Module Functions ============
    def Flight_Func(self):
        yrot, xrot = clientApi.GetEngineCompFactory().CreateRot(clientApi.GetLocalPlayerId()).GetRot()
        flightSpeed = 1
        playerComp = clientApi.GetEngineCompFactory().CreatePlayer(clientApi.GetLocalPlayerId())
        if playerComp.isSneaking() or playerComp.isSprinting(): #LShift: 16, Ctrl:17
            ym = -1 * flightSpeed
        if self.jump: #Space: 32
            ym = 1 * flightSpeed
        else:
            ym = 0
        #W: 87, A:65, S:83, D:68
        x, z = 0.0, 0.0
        if self.downkey.get("87", False): #W
            x, y, z = clientApi.GetDirFromRot((6 , xrot))
        if self.downkey.get("65", False): #A
            x, y, z = clientApi.GetDirFromRot((6 , xrot - 83.55))
        if self.downkey.get("83", False): #S
            x, y, z = clientApi.GetDirFromRot((6 , xrot - 180))
        if self.downkey.get("68", False): #D
            x, y, z = clientApi.GetDirFromRot((6 , xrot + 83.55))
        if self.downkey.get("87", False) and self.downkey.get("65", False): #W, A
            x, y, z = clientApi.GetDirFromRot((6 , xrot - 41.755))
        if self.downkey.get("87", False) and self.downkey.get("68", False): #W, D
            x, y, z = clientApi.GetDirFromRot((6 , xrot + 41.755))
        if self.downkey.get("83", False) and self.downkey.get("65", False): #S, A
            x, y, z = clientApi.GetDirFromRot((6 , xrot + 221.775))
        if self.downkey.get("83", False) and self.downkey.get("68", False): #S, D
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

    def Killaura_Func(self):
        clientApi.GetEngineCompFactory().CreatePlayer(clientApi.GetLocalPlayerId()).Swing()

    def Crasher_Func(self):
        self.NotifyToServer("CrasherEvent", {"dataA": "crash by crasher.", "dataB": "crash by crasher.", "dataC": "crash by crasher.", "dataD": "crash by crasher.", "dataE": "crash by crasher.", "dataF": "crash by crasher.", "dataG": "crash by crasher.", "dataH": "crash by crasher.", "dataI": "crash by crasher.", "dataJ": "crash by crasher.", "dataK": "crash by crasher.", "dataL": "crash by crasher.", "dataM": "crash by crasher.", "dataN": "crash by crasher.", "dataO": "crash by crasher.", "dataP": "crash by crasher.", "dataQ": "crash by crasher.", "dataR": "crash by crasher.", "dataS": "crash by crasher.", "dataT": "crash by crasher.", "dataU": "crash by crasher.", "dataV": "crash by crasher.", "dataW": "crash by crasher.", "dataX": "crash by crasher.", "dataY": "crash by crasher.", "dataZ": "crash by crasher.",})
        
    def Freecam_Func(self):
        pass
