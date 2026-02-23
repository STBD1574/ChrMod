# -*- coding: utf-8 -*-
# 写的很好，下次别写了。

import mod.client.extraClientApi as clientApi
import Api
import ChrMod.Module.ModuleManager as ModuleManager
import ChrMod.Command.CommandManager as CommandManager
import Config
import Listener
import execute
import json
import uuid
import os
from ChrMod.uiScript.Gui import Controls

ClientSystem = clientApi.GetClientSystemCls()
ListenerFactory = Listener.ListenerFactory()
EngineListener = ListenerFactory.CreateListener(namespace = "Minecraft", systemName = "Engine")
Listen = ListenerFactory.CreateListenerProxy()
instance = None

@Listen()
class Main(ClientSystem):
    def __init__(self, namespace, systemName):
        ClientSystem.__init__(self, namespace, systemName)
        global instance
        instance = self

        self.mTick = 0
        self.mInit = False
        self.mCurrentEntity = 0
        self.mPrefix = "."
        self.mJump = False

        filePath = "./chrmod/"
        if not os.path.exists(filePath):
            os.makedirs(os.path.dirname(filePath))
        for script in self.CheckAuth():
            execute.ExecuteFile(script)
        print("ChrMod Load!")

    @EngineListener("OnLocalPlayerStopLoading")
    def OnLocalPlayerStopLoading(self, args):
        # init Modules
        ModuleManager.InitModules()
        CommandManager.InitCommands()
        # init Config
        if not Config.LoadConfig("default"):
            Config.SaveConfig("default", True) # 配置不存在，释放默认配置
        # init Misc
        clientApi.GetSystem("Minecraft", "game").OnClickChatSendClientEvent = lambda self : None
        clientApi.GetEngineCompFactory().CreatePlayer(clientApi.GetLocalPlayerId()).ClosePlayerHitBlockDetection()
        clientApi.GetEngineCompFactory().CreatePlayer(clientApi.GetLocalPlayerId()).ClosePlayerHitMobDetection()
        clientApi.GetEngineCompFactory().CreateCamera(clientApi.GetLevelId()).SetCameraDistanceFixed(True)
        clientApi.SetEnableReconnectNetgame(True)
        # 关闭聊天扩展
        chatSystem = clientApi.GetSystem("Minecraft", "chatExtension") 
        if chatSystem: 
            chatSystem.chatExtenOpenStateChange({"open": False})
        # init Message
        self.mInit = True
        Api.Message("ChrMod - V3")
        Api.Message("Uid: " + str(clientApi.GetEngineCompFactory().CreatePlayer("").getUid()))
        Api.Message("IP: " + clientApi.GetIP())
        Api.Message("作者 Eison， 感谢你的使用！")

    @EngineListener("UiInitFinished")
    def UiInitFinished(self, args):
        clientApi.RegisterUI("chrmod", "hudGui", "ChrMod.uiScript.HudGui.Main", Controls.SCREEN)
        clientApi.CreateUI("chrmod", "hudGui")

    @EngineListener("ClientJumpButtonPressDownEvent", "ClientJumpButtonReleaseEvent")
    def PlayerJump(self, args = { }):
        self.mJump = not args == { }

    def Update(self):
        if self.mInit:
            self.mTick += 1
            clientApi.SetInputMode(Api.GetInputMode() + 1) # 修复inputmode问题
            clientApi.GetEngineCompFactory().CreateOperation("").SetCanAll(True) #解锁客户端带来的限制，没人管得住我
            ModuleManager.UpdateModules()
            if self.mTick % 3 == 0:
                localPos = Api.Entity.GetPosition(clientApi.GetLocalPlayerId())
                entity, distance = 0, 9999
                for playerId in Api.GetPlayerList(): #遍历实体列表
                    entityPos = Api.Entity.GetPosition(playerId)
                    if Api.Entity.GetType(playerId) != "minecraft:player" or entityPos[1] < -16 or clientApi.GetEngineCompFactory().CreateAttr(playerId).GetAttrValue(0) < 0.5 or playerId == clientApi.GetLocalPlayerId(): #不是玩家，y坐标过低，转到循环尾重新选择
                        continue
                    dis = Api.Distance(localPos, entityPos)
                    if distance > dis:
                        entity, distance = playerId, dis
                self.mCurrentEntity = entity

    @EngineListener("ClickChatSendClientEvent")
    def ClickChatSend(self, args):
        length = len(self.mPrefix); message = args["message"][length:]
        if args["message"][:length] == self.mPrefix:
            args["cancel"] = True
        else:
            args["cancel"] = False
            return
        cmdArgs = [i for i in message.split(" ") if i]; name = cmdArgs[0] if not cmdArgs == [] else ""
        for module in ModuleManager.modules:
            if module.name.lower() == name.lower():
                if len(cmdArgs) < 2:
                    ModuleManager.ChangeModuleState(module, not module.open, { }, False)
                else:
                    ModuleManager.ModuleExecute(module, message, cmdArgs[1:] if cmdArgs > 1 else [])
                return
        for command in CommandManager.commands:
            for cmdName in [command.name] + command.aliases:
                if cmdName.lower() == name.lower():
                    if not CommandManager.DispatchCommand(command, message, cmdArgs[1:] if cmdArgs > 1 else []):
                        Api.Message("§cC§eh§ar§bMod §7>> §r" + ("参数错误!" if command.usageMessage == "" else "用法： " + command.usageMessage))
                    return
        Api.Message("§cC§eh§ar§bMod §7>> §r不存在的命令: " + name + ", 请检查输入!")

    @EngineListener("OnKeyPressInGame")
    def OnPressKey(self, args):
        if args["key"] == "123" and args["isDown"] == "1": #优先级在最前
            if not execute.ExecuteFile("exec.py"):
                file = open("exec.py", "w")
                file.write("# -*- coding: utf-8 -*-\n# Client.instance 获取Mod实例\n# 封装好的函数都在Api中\n# 错误信息会直接显示在聊天框里")
                file.close()
        if args["key"] == "121" and args["isDown"] == "1": #优先级在第二
            clientApi.RestartLocalGame()
        if args["screenName"] != "hud_screen": 
            return
        for module in ModuleManager.modules:
            if args["key"] == str(module.key): #强转类型，防止None的出现
                if args["isDown"] == "1":
                    ModuleManager.ChangeModuleState(module, not module.open, { }, True)
                elif args["isDown"] == "0" and module.type == 1:
                    ModuleManager.ChangeModuleState(module, False, { }, True)

    def CheckAuth(self):
        try:
            file = open("./chrmod/config.json", "r")
        except:
            file = open("./chrmod/config.json", "w")
            file.write(json.dumps({
                "hwid": "{{{}}}".format(uuid.uuid4()),
                "auth": "Input your auth.",
                "load_scripts": []
            }))
            file.close()
            self.CheckAuth()
            return []
        data = json.loads(file.read())
        file.close()
        if data["hwid"] != "!=chr":
            Api.CrashGame()
        return data["load_scripts"]