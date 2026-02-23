# -*- coding: utf-8 -*-
# author Eison 
# 2024/04/20

from ..importer import Module

_voice_trans  = Module('_voice_trans')
gui           = Module('gui')
entity_module = Module('entity_module')
_crashhelper  = Module('_crashhelper')
clientlevel   = Module('clientlevel')
game_ruler    = Module('game_ruler')

MESSAGE_PREFIX = '§cC§eh§ar§bMod §7>§r '

def GetPlayerList(): 
    # type: () -> list[str]
    return clientlevel.get_player_list()

def SendChatMsg(text): 
    #type: (str) -> None
    _voice_trans.sendChatMsg(text)

def DisplayClientMessage(*message): 
    #type: (any) -> None
    msg = ''.join(str(i) for i in message)
    while len(msg) > 0:
        gui.set_left_corner_notify_msg(msg[:600])
        msg = msg[600:]
    
def GetLocalPlayerId(): 
    # type: () -> str
    return entity_module.get_local_player_id()

def AddRepeatedTimer(delay, func, *args, **kwargs): 
    # type: (float, function, *any, **any) -> any
    game = Module('common.game')
    return game.GetClient().GetClientModTimer().addRepeatTimer(delay, func, *args, **kwargs) 

def AddTimer(delay, func, *args, **kwargs): 
    # type: (float, function, *any, **any) -> any
    game = Module('common.game')
    return game.GetClient().GetClientModTimer().addTimer(delay, func, *args, **kwargs)

def CancelTimer(timer): 
    # type: (any) -> None
    game = Module('common.game')
    game.GetClient().GetClientModTimer().cancel(timer)
    
def StartCoroutine(iterOrFunc, callback = None): 
    # type: (any, function) -> any
    coroutineMgr = Module('mod.client.clientCoroutineMgr')
    return coroutineMgr.instance().StartCoroutine(iterOrFunc, callback)

def StopCoroutine(iter): 
    # type: (any) -> bool
    coroutineMgr = Module('mod.client.clientCoroutineMgr')
    return coroutineMgr.instance().StopCoroutine(iter)

def GetInputVector(): 
    # type: () -> tuple[float, float]
    return gui.get_input_vector()

def ShowHealthBar(show): 
    # type: (bool) -> bool
    return gui.show_health(show)

def Crash(): # type: () -> None
    _crashhelper.test_crash()

def Disconnect(message): # type: (str) -> bool
    ''' 这个函数在单机存档下可以毁档？？ '''
    return clientlevel.disconnect_game(message)

def DisplayMessage(msgType, msg, author, color): # type: (int, str, str, str) -> bool
    '''
    这真是一个神秘的函数，msgType值：
    0 直接在聊天栏输出
    1 模拟玩家发言，玩家名是author
    2 同0
    3 popup有两行，第一行author，第二行msg
    4 不知道是啥，没背景
    5 是tip，在actionbar下方
    6 同0
    7 悄悄说，与1相似
    8 同0
    '''
    return clientlevel.display_message(msgType, msg, author, color)

def GetCurrentDimension(): # type: () -> int
    ''' 客户端未登录完成或正在切维度时返回-1 '''
    return clientlevel.get_current_dimension()

def GetFPS(): # type: () -> float
    return game_ruler.get_Fps()

def ClearTitle(): # type: () -> bool
    return clientlevel.clear_title()