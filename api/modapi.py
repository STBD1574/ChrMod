# -*- coding: utf-8 -*-
# author Eison 
# 2024/04/20

from ..importer import Module

eventUtil    = Module("mod.common.eventUtil")
_pynetmodule = Module("_pynetmodule")
msgpack      = Module("msgpack")
_setting     = Module("_setting")

def GetModList(): # type: () -> dict[str, any]
    """ it is an OrderedDict. """
    modSysReg = Module("common.system.systemRegister")
    return modSysReg.client.systemInstances

def GetSystem(namespace, systemName): # type: (str, str) -> any | None
    return GetModList().get(namespace + ":" + systemName, None)

def PackPyRpcPacket(namespace, systemName, eventName, eventData): # type: (str, str, str, any) -> str
    # like ("ModEventC2S", [namespace, systemName, eventName, eventData], None, xxx)
    return msgpack.packb(("ModEventC2S", (namespace, systemName, eventName, eventData), None), use_bin_type=False, strict_types=True, default=lambda __object: {"__type__": "tuple", "value": list(__object)} if isinstance(__object, tuple) else __object)

def SendPyRpcPacket(eventData): # type: (str) -> None
    _pynetmodule.send2server(98247598, eventData, len(eventData))

def ListenForEvent(namespace, systemName, eventName, instance, func, priority=0, isSystem=True): # type: (str, str, str, any, function, int, bool) -> None
    eventUtil.instance.ListenForEventClient(namespace, systemName, eventName, instance, func, priority, isSystem)

def UnListenForEvent(namespace, systemName, eventName, instance, func, priority=0, isSystem=True): # type: ignore # type: (str, str, str, any, function, int, bool) -> None
    eventUtil.instance.UnListenForEventClient(namespace, systemName, eventName, instance, func, priority, isSystem)

def ListenForEngineClient(eventName, instance, func, priority=0, isSystem=True): # type: (str, any, function, int, bool) -> None
    eventUtil.instance.ListenForEngineClient(eventName, instance, func, priority, isSystem)

def UnListenForEngineClient(eventName, instance, func, priority=0, isSystem=True): # type: ignore # type: (str, any, function, int, bool) -> None
    eventUtil.instance.UnListenForEngineClient(eventName, instance, func, priority, isSystem)

def GetPlatform(): # type: () -> int
    """ 导入前面不能加mod 不然返回-1 """
    modGameCfg = Module("common.gameConfig")
    return modGameCfg.RUNTIME_PLATFORM

def SetPlatform(platform): # type: (int) -> None
    """ 导入前面不能加mod 不然返回-1 """
    modGameCfg = Module("common.gameConfig")
    modGameCfg.RUNTIME_PLATFORM = platform

def GetInputMode(): # type: () -> int
    return _setting.get_toggle_option("INPUT_MODE")