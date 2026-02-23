# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
from ChrMod.Module.ModuleManager import Module, ModuleType
from mod.common.minecraftEnum import KeyBoardType
import ChrMod.Client as Client
import math

class TPAura(Module):
    def __init__(self):
        Module.__init__(self, "TPAura", "环绕某一个玩家。", ModuleType.COMBAT, False, KeyBoardType.KEY_PG_UP)
        self.Game = clientApi.GetEngineCompFactory().CreateGame("")
        self.Timer = None
        self.range = 0

    def OnEnable(self):
        self.Timer = self.Game.AddRepeatedTimer(0.001, self.TPAura_Func)

    def OnDisable(self):
        self.Game.CancelTimer(self.Timer)

    def TPAura_Func(self):
        if Client.instance.mCurrentEntity == 0: #无实体
            return
        if self.range > 359.0:
            self.range = 0.0
        self.range += 25.6
        range2 = self.range
        myPos = clientApi.GetEngineCompFactory().CreatePos(clientApi.GetLocalPlayerId()).GetPos()
        nePos = ()
        x, y, z = clientApi.GetEngineCompFactory().CreatePos(Client.instance.mCurrentEntity).GetPos()
        nePos_x , nePos_z = self.GetCirclePos(x, z, 2, range2)
        nePos = (nePos_x, y, nePos_z)
        mPos = self.MotionPosCountYadd(nePos, myPos, 2.5)
        nPos = self.MotionPosRectify(mPos)
        clientApi.GetEngineCompFactory().CreateActorMotion(clientApi.GetLocalPlayerId()).SetMotion(nPos)

    def GetCirclePos(self, xc, zc, distancec, angle):
        ''' [AMCPK] 向量运算 x坐标，z坐标，距离，角度 '''
        posx = float(xc) + float(distancec) * math.cos(float(angle) * 3.1415926 / 180)
        posz = float(zc) + float(distancec) * math.sin(float(angle) * 3.1415926 / 180)
        return posx, posz

    def MotionPosCountYadd(self, enemyPos, myPos, yAdd):
        ''' [AMCPK] 向量坐标运算，y轴增加 '''
        enemyPos = list(enemyPos)
        myPos = list(myPos)
        for i in range(3):
            Pc_x = (enemyPos[0] - myPos[0]) * 0.496
            Pc_y = (enemyPos[1] - myPos[1] + yAdd) * 0.496
            Pc_z = (enemyPos[2] - myPos[2]) * 0.496
            Pc = [Pc_x , Pc_y , Pc_z]
        return tuple(Pc)

    def MotionPosRectify(self, mPos):
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