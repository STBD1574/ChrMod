# -*- coding: utf-8 -*-

from ...api import textboard, entity, modapi, client
from ..module import Module, Category

class NameTag(Module):
    def __init__(self):
        Module.__init__(self, 'NameTag', '显示玩家名称标签。', Category.VISUAL, None)

        self.tagToPlayers = { }

    def OnEnable(self):
        modapi.ListenForEngineClient('AddPlayerAOIClientEvent', self, self.AddPlayerAOIClientEvent, 10)
        modapi.ListenForEngineClient('RemovePlayerAOIClientEvent', self, self.RemovePlayerAOIClientEvent, 10)

        for playerId in client.GetPlayerList():
            self.CreateTag(playerId)

    def OnDisable(self):
        modapi.UnListenForEngineClient('AddPlayerAOIClientEvent', self, self.AddPlayerAOIClientEvent, 10)
        modapi.UnListenForEngineClient('RemovePlayerAOIClientEvent', self, self.RemovePlayerAOIClientEvent, 10)

        for tagId in self.tagToPlayers.itervalues():
            textboard.RemoveTextBoard(tagId)
        
        self.tagToPlayers = { }

    def CreateTag(self, playerId):
        tagId = textboard.CreateTextBoardInWorld(entity.GetName(playerId), (1, 1, 1, 1), (0, 0, 0, 0.5), True)
        
        textboard.SetBoardBindEntity(tagId, playerId, (0, 0.75, 0), (0, 0, 0))
        textboard.SetBoardScale(tagId, (2, 2))

        self.tagToPlayers[playerId] = tagId

    def AddPlayerAOIClientEvent(self, args):
        self.CreateTag(args['playerId'])

    def RemovePlayerAOIClientEvent(self, args):
        playerId = args['playerId']

        if playerId in self.tagToPlayers:
            tagId = self.tagToPlayers[playerId]
            textboard.RemoveTextBoard(tagId)
            del self.tagToPlayers[playerId]