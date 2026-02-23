# -*- coding: utf-8 -*-
# author Eison
# 2024/07/14

from ..module import Module, Category, KeyBoardType
from ...api import entity, client, math

class Aimbot(Module):
	def __init__(self):
		Module.__init__(self, "Aimbot", "自动瞄准。", Category.COMBAT, KeyBoardType.KEY_PERIOD)

		self.timer = None

	def OnEnable(self):
		self.localplayerId = client.GetLocalPlayerId()
		self.timer = client.AddRepeatedTimer(0.001, self.Aimbot_Func)

	def OnDisable(self):
		client.CancelTimer(self.timer)

	def Aimbot_Func(self):
		minDis, targetId, fromPos = 99999, None, entity.GetPosition(self.localplayerId)
		for playerId in client.GetPlayerList():
			if entity.IsAlive(playerId) and playerId != self.localplayerId:
				pos, dis = entity.GetPosition(playerId), entity.GetDistance(self.localplayerId, playerId)
				if dis < minDis:
					minDis, targetId, targetPos = dis, playerId, pos

		if not targetId:
			return

		direction = (targetPos[0] - fromPos[0], targetPos[1] - fromPos[1], targetPos[2] - fromPos[2])
		targetRot = math.GetRotationFromDirection(direction)
		curRot = entity.GetRotation(self.localplayerId)

		targetRot = (targetRot[0] % 360, targetRot[1] % 360)
		curRot = (curRot[0] % 360, curRot[1] % 360)

		step = [(targetRot[0] - curRot[0]) % 360, (targetRot[1] - curRot[1]) % 360]
		result = ((curRot[0] + step[0]) % 360, (curRot[1] + step[1]) % 360)

		entity.SetRotation(self.localplayerId, result)