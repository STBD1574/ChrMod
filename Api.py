# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
import Client
import string
import random
import gui
import _voice_trans
import math

def instance():
    #type: () -> Client.Main
    ''' 获取模组实例 '''
    return Client.instance

def list_remove_empty(list):
    #type: (list) -> list
    ''' 列表去空项 '''
    a = [i for i in list if i]
    print(a)
    return a

def SendMessage(text):
    # type: (any) -> bool
    ''' 向本地玩家发送聊天栏消息，不经过屏蔽词检测 '''
    strtext = str(text)
    if len(strtext) > 600:
        for i in range((len(strtext) / 600) + 1):
            length = (i + 1) * 600
            gui.set_left_corner_notify_msg(strtext[i * 600 : len(strtext) if length > len(strtext) else length])
    else:
        gui.set_left_corner_notify_msg(strtext)

def Dist(x1, y1, z1, x2, y2, z2):
    #type: (float, float, float, float, float, float) -> float
	''' 运算3维空间距离，返回float '''
	return float('%.1f' % ((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2) ** 0.5)

def GetPlayerList(hasSelf = True, entity = clientApi.GetLocalPlayerId()):
    #type: (bool, str) -> list[str]
    ''' 获取玩家列表 '''
    list = clientApi.GetPlayerList()
    if len(list) < 2 if hasSelf else 1: #新的不行上旧的
        px, py, pz = clientApi.GetEngineCompFactory().CreatePos(entity).GetPos()
        for id in clientApi.GetEngineCompFactory().CreateGame(0).GetEntityInArea(entity, (px - 128, py - 128, pz - 128), (px + 128, py + 128, pz + 128)):
            if clientApi.GetEngineCompFactory().CreateEngineType(id).GetEngineTypeStr() == 'minecraft:player' and id != entity if hasSelf else True:
                list.append(id)
    return list

def GetClosestPlayer(entity, hasSelf = True):
    #type: (str | int, bool) -> tuple[int, float]
    ''' 获取距离entity最近的玩家，返回playerid和距离 '''
    x, y, z = clientApi.GetEngineCompFactory().CreatePos(entity).GetPos()
    player = -2
    Distance = 2147483647
    list = GetPlayerList(entity)
    for id in list:
        x2, y2, z2 = clientApi.GetEngineCompFactory().CreatePos(id).GetPos()
        dis2 = Dist(x, y, z, x2, y2, z2)
        if dis2 < Distance and id != clientApi.GetLocalPlayerId() if hasSelf else True:
            Distance = dis2
            player = id
    return player, Distance

def PlaySound(soundId, playerId = None):
    #type: (str, str) -> str
    ''' 为某个玩家播放场景音效 '''
    return clientApi.GetEngineCompFactory().CreateCustomAudio(clientApi.GetLocalPlayerId()).PlayCustomMusic(soundId, entityId = playerId)

def GetSystemEvents(nameSpace, systemName):
    #type: (str, str) -> list[str]
    ''' 获取某个system监听的所有事件 '''
    system = clientApi.GetSystem(nameSpace, systemName)
    return system.nameToListenEvents.keys() if system else None

def GetRandomText(length = 8):
    #type: (int) -> str
    ''' 获取一段随机文本 '''
    return ''.join(random.sample(string.ascii_letters + string.digits, length))

def SendChatMsg(text):
    #type: (str) -> None
    ''' 在聊天栏说话 '''
    _voice_trans.sendChatMsg(text)

def GetCirclePos(xc, zc, distancec, angle):
    #type: (float, float, float, float) -> tuple[float, float]
    ''' [AMCPK] 向量运算 x坐标，z坐标，距离，角度 '''
    posx = float(xc) + float(distancec) * math.cos(float(angle) * 3.1415926 / 180)
    posz = float(zc) + float(distancec) * math.sin(float(angle) * 3.1415926 / 180)
    return posx, posz

def MotionPosCountYadd(enemyPos, myPos, yAdd):
    #type: (float, float, float) -> tuple
    ''' [AMCPK] 向量坐标运算，y轴增加 '''
    enemyPos = list(enemyPos)
    myPos = list(myPos)
    for i in range(3):
        Pc_x = (enemyPos[0] - myPos[0]) * 0.496
        Pc_y = (enemyPos[1] - myPos[1] + yAdd) * 0.496
        Pc_z = (enemyPos[2] - myPos[2]) * 0.496
        Pc = [Pc_x , Pc_y , Pc_z]
    return tuple(Pc)

def MotionPosRectify(mPos):
    #type: (list) -> tuple
    ''' [AMCPK] 向量坐标纠正 '''
    mPos = list(mPos)
    nPos = [1 ,1, 1]
    for i in range(3):
        if mPos[i] > 3.0:
            nPos[i] = 3.0
        elif mPos[i] < -3.0:
            nPos[i] = -3.0
        else:
            nPos[i] = mPos[i]
    return tuple(nPos)
