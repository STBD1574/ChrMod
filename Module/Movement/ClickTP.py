# -*- coding: utf-8 -*-
from ChrMod.Module.ModuleManager import Module
from ChrMod.Module.ModuleManager import ModuleType
from mod.common.minecraftEnum import KeyBoardType
import mod.client.extraClientApi as clientApi
import ChrMod.Api as Api

class ClickTP(Module):
    def __init__(self):
        Module.__init__(self, "ClickTP", "点击传送。", ModuleType.MOVEMENT, False, KeyBoardType.KEY_END)

    def OnEnable(self):
        Api.ListenForEvent("Minecraft", "Engine", "RightClickBeforeClientEvent", self, self.OnEvent, 10, True)
        Api.ListenForEvent("Minecraft", "Engine", "HoldBeforeClientEvent", self, self.OnEvent, 10, True)

    def OnDisable(self):
        Api.UnListenForEvent("Minecraft", "Engine", "RightClickBeforeClientEvent", self, self.OnEvent, 10, True)
        Api.UnListenForEvent("Minecraft", "Engine", "HoldBeforeClientEvent", self, self.OnEvent, 10, True)


    def OnEvent(self, args):
        dict = clientApi.GetEngineCompFactory().CreateCamera(clientApi.GetLevelId()).PickFacing()
        if dict['type'] == 'Block':
            x = (dict['x'] + 1 if dict['face'] == 5 else dict['x'] - 1 if dict['face'] == 4 else dict['x']) + 0.5 #方块朝向算法
            y = dict['y'] + 3 if dict['face'] == 1 else dict['y'] if dict['face'] == 0 else dict['y'] + 2
            z = (dict['z'] + 1 if dict['face'] == 3 else dict['z'] - 1 if dict['face'] == 2 else dict['z']) + 0.5
            Api.Teleport((x, y, z))
            Api.Message('§aTeleport to §7x: ' + str(x) + ' y: ' + str(y) + ' z: ' + str(z))
        elif dict['type'] == 'Entity':
            x, y, z = clientApi.GetEngineCompFactory().CreatePos(dict['entityId']).GetPos()
            Api.Teleport((x, y + 2, z))
            Api.Message('§aTeleport to §7' + Api.Entity.GetName(dict['entityId']))