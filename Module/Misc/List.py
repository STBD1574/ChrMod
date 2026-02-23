# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
from ChrMod.Module.ModuleManager import Module
from ChrMod.Module.ModuleManager import ModuleType
from mod.common.minecraftEnum import KeyBoardType
import ChrMod.Api as Api

class List(Module):
    def __init__(self):
        Module.__init__(self, "List", "获取玩家列表。", ModuleType.MISC, False, KeyBoardType.KEY_TAB, 2)

    def OnEnable(self):
        Api.Message("§cC§eh§ar§bMod §7>> §r玩家列表")
        for entityId in Api.GetPlayerList():
            Api.Message("§cC§eh§ar§bMod §7>> §r" + Api.Entity.GetName(entityId) + " §rPosition: " + str(tuple([round(i, 1) for i in clientApi.GetEngineCompFactory().CreatePos(entityId).GetPos()])))
        return True

