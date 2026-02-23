# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
from ChrMod.Module.ModuleManager import Module
from ChrMod.Module.ModuleManager import ModuleType
import ChrMod.Api as Api

class HighJump(Module):
    def __init__(self):
        Module.__init__(self, "HighJump", "高跳。", ModuleType.MOVEMENT, False, None, 2)
        Api.ListenForEvent("Minecraft", "Engine", "ClientJumpButtonPressDownEvent", self, self.OnEvent)
        self.Motion = clientApi.GetEngineCompFactory().CreateActorMotion(clientApi.GetLocalPlayerId())
        self.High = 1.2 

    def OnEvent(self, args):
        if self.open:
            args['continueJump'] = False
            if clientApi.GetEngineCompFactory().CreateAttr(clientApi.GetLocalPlayerId()).isEntityOnGround():
                x, y, z = self.Motion.GetMotion()
                self.Motion.SetMotion((x, self.High, z))

    def Execute(self, label, args):
        try:
            self.High = float(args[0])
            Api.Message("§cC§eh§ar§bMod §7>> §r修改成功!")
        except:
            return False
        
