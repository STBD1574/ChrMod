# -*- coding: utf-8 -*-
# author Eison
# 2024/07/15

from ..module import Module, Category, KeyBoardType
from ...api import client, entity, math, localplayer

class Killaura(Module):
	def __init__(self):
		Module.__init__(self, "Killaura", "杀戮光环。", Category.COMBAT, KeyBoardType.KEY_R)

		self.timer = None
		self.localplayer = -2

	def OnEnable(self):
		self.localplayer = client.GetLocalPlayerId()
		self.timer = client.AddRepeatedTimer(0.001, self.Killaura_Func)

	def OnDisable(self):
		if self.timer:
			client.CancelTimer(self.timer)

		localplayer.UnDepartCamera()

	def Killaura_Func(self):
		import mod.client.extraClientApi as clientApi
		minDis, targetId, fromPos = 99999, None, entity.GetPosition(self.localplayer)
		for playerId in clientApi.GetEngineActor().keys():
			if not entity.IsAlive(playerId) or playerId == self.localplayer:
				continue

			pos, dis = entity.GetPosition(playerId), entity.GetDistance(self.localplayer, playerId)
			if dis < minDis:
				minDis, targetId, targetPos = dis, playerId, pos

		if not targetId:
			return

		direction = (targetPos[0] - fromPos[0], targetPos[1] - fromPos[1], targetPos[2] - fromPos[2])
		targetRot = math.GetRotationFromDirection(direction)
		curRot = entity.GetRotation(self.localplayer)

		targetRot = (targetRot[0] % 360, targetRot[1] % 360)
		curRot = (curRot[0] % 360, curRot[1] % 360)

		step = [(targetRot[0] - curRot[0]) % 360, (targetRot[1] - curRot[1]) % 360]
		result = ((curRot[0] + step[0]) % 360, (curRot[1] + step[1]) % 360)

		localplayer.DepartCamera()
		entity.SetRotation(self.localplayer, result)

		if localplayer.GetPerspective() != 1: # 第三人称有单独的实现
			localplayer.UnDepartCamera()

