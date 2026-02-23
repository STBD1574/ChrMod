# -*- coding: utf-8 -*-
from ChrMod.Module.ModuleManager import Module, ModuleType
import mod.common.network.defaultrpc as rpc
import mod.client.extraClientApi as clientApi
import ChrMod.Api as Api
import json

class Event:
    def __init__(self, namespace, systemName, eventName, funcName): #type: (str, str, str, str) -> None
        self.namespace, self.systemName, self.eventName, self.funcName = namespace, systemName, eventName, funcName

    def OnEvent(self, eventData = { }):
        if self.namespace == "Minecraft" and self.systemName == "Engine":
            if not instance.Engine:
                return
        if instance.Logger:
            if instance.Message:
                Api.Message("§cC§eh§ar§bMod §7>> §rModEventS2C namespace: " + self.namespace + " systemName: " + self.systemName + " eventName: " + self.eventName + " funcName: " + self.funcName + " eventData: " + json.dumps(eventData, encoding = "utf-8", ensure_ascii = False))
            if instance.Write:
                file = open("rpclog.txt", "a")
                file.write("ModEventS2C namespace: " + self.namespace + " systemName: " + self.systemName + " eventName: " + self.eventName + " funcName: " + self.funcName + " eventData: " + json.dumps(eventData, encoding = "utf-8", ensure_ascii = False) + "\n\n")
                file.close()


class RpcLogger(Module):
    def __init__(self):
        Module.__init__(self, "RpcLogger", "PyRpc数据包记录器，支持写入至文件中（双向记录）。", ModuleType.MISC, False, "", 0, ".rpclogger <write> <block> <engine> <message>")
        global instance
        instance = self
        self.Logger = False
        self.Write = True
        self.Block = False #目前只支持客户端到服务端的rpc拦截
        self.Engine = False #是否监听来自引擎的事件
        self.Message = True #是否显示消息

        self.InitLogger()

    def OnEnable(self):
        self.Logger = True

    def OnDisable(self):
        self.Logger = False

    def CreateLogger(self): #type: () -> None
        rpc.CServerRpc().ModEventC2S # init ModEventC2S
        original_ModEventC2S = rpc.CServerRpc.ModEventC2S
        def ModEventC2S(selfs, namespace, systemName, eventName, eventData):
            if namespace == "Minecraft" and systemName == "Engine":
                if not instance.Engine:
                    return
            if self.Logger:
                if self.Message:
                    Api.Message("§cC§eh§ar§bMod §7>> §rModEventC2S namespace: " + namespace + " systemName: " + systemName + " eventName: " + eventName + " eventData: " + json.dumps(eventData, encoding = "utf-8", ensure_ascii = False))
                if self.Write:
                    file = open("rpclog.txt", "a")
                    file.write("ModEventC2S namespace: " + namespace + " systemName: " + systemName + " eventName: " + eventName + " eventData: " + json.dumps(eventData, encoding = "utf-8", ensure_ascii = False) + "\n\n")
                    file.close()
                if self.Block:
                    Api.Message("§cC§eh§ar§bMod §7>> §r已拦截事件: " + eventName)
                    return
            original_ModEventC2S(selfs, namespace, systemName, eventName, eventData)
        rpc.CServerRpc.ModEventC2S = ModEventC2S

    def CreateListener(self, system): #type: (clientApi.ClientSystem) -> None
        for events in system.nameToListenEvents.values():
            for event in events:
                if not (event.namespace == "Minecraft" and event.systemName == "Engine" and event.eventName == "OnScriptTickClient"): #不监听这个事件，不然会刷屏
                    instance = Event(event.namespace, event.systemName, event.eventName, event.funcName.__name__)
                    Api.ListenForEvent(event.namespace, event.systemName, event.eventName, instance, instance.OnEvent, 10, True)

    def InitLogger(self):
        self.CreateLogger()
        def Coroutine():
            for system in Api.GetModList().values(): #C2S的修改
                self.CreateListener(system)
                yield
        clientApi.StartCoroutine(Coroutine)

    def Execute(self, label, args): #type: (str, list[str]) -> bool
        if len(args) > 1:
            self.Write = args[0].lower() == "true"
            self.Block = args[1].lower() == "true"
            self.Engine = args[2].lower() == "true"
            self.Message = args[3].lower() == "true"
            Api.Message("§cC§eh§ar§bMod §7>> §r修改成功!")
        else:
            return False