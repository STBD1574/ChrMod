# -*- coding: utf-8 -*-

import math
from ..module import Module, Category, KeyBoardType
from ...api import client, entity

class TPAura(Module):
	def __init__(self):
		Module.__init__(self, "TPAura", "环绕某一个玩家。", Category.COMBAT, KeyBoardType.KEY_PG_UP)
		self.timer = None
		self.range = 0

	def OnEnable(self):
		self.localPlayerId = client.GetLocalPlayerId()
		self.timer = client.AddRepeatedTimer(0.001, self.TPAura_Func)

	def OnDisable(self):
		client.CancelTimer(self.timer)

	def TPAura_Func(self):
		minDis, targetId = 99999, None
		for playerId in client.GetPlayerList():
			if entity.IsAlive(playerId) and playerId != self.localPlayerId:
				dis = entity.GetDistance(self.localPlayerId, playerId)
				if dis < minDis:
					minDis, targetId, = dis, playerId

		if not targetId:
			return
		  
		if self.range > 359.0:
			self.range = 0.0
		self.range += 25.6
		range2 = self.range
		myPos = entity.GetPosition(self.localPlayerId)
		nePos = ()
		x, y, z = entity.GetPosition(targetId)
		nePos_x , nePos_z = self.GetCirclePos(x, z, 2, range2)
		nePos = (nePos_x, y, nePos_z)
		mPos = self.MotionPosCountYadd(nePos, myPos, 2.5)
		nPos = self.MotionPosRectify(mPos)

		entity.SetMotion(self.localPlayerId, nPos)

	def GetCirclePos(self, xc, zc, distancec, angle):
		posx = float(xc) + float(distancec) * math.cos(float(angle) * math.pi / 180)
		posz = float(zc) + float(distancec) * math.sin(float(angle) * math.pi / 180)
		return posx, posz

	def MotionPosCountYadd(self, enemyPos, myPos, yAdd):
		enemyPos = list(enemyPos)
		myPos = list(myPos)
		for i in range(3):
			Pc_x = (enemyPos[0] - myPos[0]) * 0.496
			Pc_y = (enemyPos[1] - myPos[1] + yAdd) * 0.496
			Pc_z = (enemyPos[2] - myPos[2]) * 0.496
			Pc = [Pc_x , Pc_y , Pc_z]
		return tuple(Pc)

	def MotionPosRectify(self, mPos):
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