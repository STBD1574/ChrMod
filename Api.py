# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
import string
import random
import gui
import _voice_trans
import math
import clientlevel
from collections import OrderedDict
import time
import mod.common.eventUtil as eventUtil
import _crashhelper
import QSecImp
import _setting

class Entity: # about Entity
    @staticmethod
    def GetType(entityId): #type: (str | int) -> str
        ''' 获取实体类型 '''
        return clientApi.GetEngineCompFactory().CreateEngineType(entityId).GetEngineTypeStr()

    @staticmethod
    def GetName(entityId, useLang = False): #type: (str | int, bool) -> str
        ''' 获取实体名称 '''
        name = clientApi.GetEngineCompFactory().CreateName(entityId).GetName()
        return clientApi.GetEngineCompFactory().CreateGame("").GetChinese(Entity.GetType(entityId).replace("minecraft:", "entity.") + ".name") if useLang and not name else name

    @staticmethod
    def GetPosition(entityId): #type: (str | int) -> tuple[float, float, float]
        ''' 获取实体位置 '''
        return clientApi.GetEngineCompFactory().CreatePos(entityId).GetPos()
    
class Debug: #测试类，一般不公开
    @staticmethod
    def RunInServer(script): #type: (str) -> None
        ''' safaia in server: 无效 '''
        ModEventC2S("Minecraft", "safaia", "SafaiaRunServer", script)

    @staticmethod
    def TestEvent(args): #type: (any) -> None
        ''' ChrMod Test Event: debug '''
        ModEventC2S("ChrMod", "qwq", "awa", args)

def TipMessage(text): #type: (any) -> bool
    ''' 在本地玩家的物品栏上方弹出tip类型通知，不经过屏蔽词检测 '''
    return clientlevel.show_tip_message(str(text))

def Message(text): # type: (any) -> None
    ''' 向本地玩家发送聊天栏消息，不经过屏蔽词检测 '''
    msg = str(text)
    while len(msg) > 0:
        gui.set_left_corner_notify_msg(msg[:600])
        msg = msg[600:]

def Distance(pos1, pos2): #type: (tuple[float, float, float], tuple[float, float, float]) -> float
	''' 运算3维空间距离，返回float '''
	return float('%.1f' % ((pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1]) ** 2 + (pos2[2] - pos1[2]) ** 2) ** 0.5)

def GetPlayerList(valid = True): #type: (bool) -> list[str]
    ''' 获取实体列表 '''
    return [i for i in clientApi.GetPlayerList() if (Entity.GetType(i) and valid)] if valid else clientApi.GetPlayerList()

def PlayMusic(name, pos = (0, 0, 0), volume = 1, pitch = 1, loop = False, entityId = None): # type: (str, tuple[float,float,float], float, float, bool, str) -> str
    ''' 播放场景音效，包括原版音效及自定义音效 '''
    return clientApi.GetEngineCompFactory().CreateCustomAudio(clientApi.GetLocalPlayerId()).PlayCustomMusic(name, pos, volume, pitch, loop, entityId)

def GetModEvents(mod): #type: (clientApi.ClientSystem) -> dict
    ''' 获取某个mod监听的所有事件 '''
    return mod.nameToListenEvents if mod else None

def GetRandomString(length): #type: (int) -> str
    ''' 获取一段随机文本 '''
    return ''.join(random.sample(string.ascii_letters + string.digits, length))

def SendChatMsg(text): #type: (str) -> None
    ''' 在聊天栏说话 '''
    _voice_trans.sendChatMsg(text)

def Attack(): #type: () -> None
    ''' 本地玩家攻击 '''
    import localplayermodule
    localplayermodule.local_player_begin_swing()

def Teleport(position): #type: (tuple[float, float, float]) -> bool
    ''' 本地玩家传送 '''
    return clientApi.GetEngineCompFactory().CreateCamera(clientApi.GetLevelId()).SetCameraPos(position)

def ModEventC2S(namespace, systemName, eventName, eventData): #type: (str, str, str, str) -> None
    ''' 客户端发送事件到服务器 '''
    import mod.common.network.defaultrpc as rpc
    rpc.CServerRpc().ModEventC2S(namespace, systemName, eventName, eventData)

def PostEvent(namespace, systemName, eventName, eventData): #type: (str, str, str, dict) -> None
    ''' 本地广播事件，客户端system广播的事件仅客户端system能监听，服务器system广播的事件仅服务端system能监听。 '''
    from common.system.systemRegister import client
    eventID = namespace + ":" + systemName + ":" + eventName
    client.PostEvent(eventID, eventData)

def GetModList(): #type: () -> OrderedDict[str, clientApi.ClientSystem]
    ''' 获取客户端加载的mod列表 '''
    import common.system.systemRegister as modSysReg
    return modSysReg.client.systemInstances

def SendCommand(command): #type: (str) -> None
    ''' 执行游戏内命令 '''
    clientApi.GetSystem('Minecraft', 'aiCommand').SendCommand(command)

def GetCurrentTime(): #type: () -> int
    ''' 获取现行时间。与time.time()不同的是，这个是返回一个整数。 '''
    return int(time.time() * 1000.0)

def ListenForEvent(namespace, systemName, eventName, instance, func, priority=0, isSystem=True): #type: (str, str, str, any, function, int, bool) -> None
    ''' 监听事件，只不过这个事件监听不依赖system. '''
    eventUtil.instance.ListenForEventClient(namespace, systemName, eventName, instance, func, priority, isSystem)

def UnListenForEvent(namespace, systemName, eventName, instance, func, priority=0, isSystem=True): #type: (str, str, str, any, function, int, bool) -> None
    ''' 反监听事件，跟上面同理. '''
    eventUtil.instance.UnListenForEventClient(namespace, systemName, eventName, instance, func, priority, isSystem)

def CrashGame(): #type: () -> None
    ''' 崩掉客户端 '''
    _crashhelper.test_crash()
    qsec = QSecImp.getInstance()
    base = qsec.PyGetModuleBase('libminecraftpe.so')
    qsec.PyCallFunc('libc.so', 'mprotect', base, 268435456, 1)

def GetInputMode(): #type: () -> int
    ''' 获取inputmode '''
    return _setting.get_toggle_option("INPUT_MODE")

def Import(moduleName): #type: (str) -> any
    ''' 导入指定模块，以备不时之需 '''
    implibObj = None
    for c1 in ('').__class__.__mro__:
        if c1.__name__ == 'object':
            implibObj = c1
            break
    for c2 in implibObj.__subclasses__():
        if c2.__name__ == '_IterationGuard':
            implibObj = c2
            break
    implibObj = implibObj.__init__.__globals__['__builtins__']['__import__']('importlib')
    return implibObj.import_module(moduleName)