# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
from ChrMod.Module.ModuleManager import Module
from ChrMod.Module.ModuleManager import ModuleType
from mod.common.minecraftEnum import KeyBoardType
import ChrMod.Api as Api

class Disabler(Module):
    def __init__(self):
        Module.__init__(self, "Disabler", "绕过某些反作弊的检测。", ModuleType.MISC, True, KeyBoardType.KEY_DELETE)
        self.original_NotifyToServer = None
        self.Message = False

    def OnEnable(self):
        Zmeng = clientApi.GetSystem("AntiCheatingMod", "AntiCheatingClientSystem")
        if not Zmeng:
            self.open = False
            return True
        self.original_NotifyToServer = Zmeng.NotifyToServer
        def NotifyToServer(event_name, event_data):
            if event_name == "KickSelf": #绕过逐梦踢出自己
                if self.Message:
                    Api.Message("§cC§eh§ar§bMod §7>> §r逐梦启元尝试踢出你，因为 " + event_data["reason"])
                return
            if event_name == "Ping": #绕过逐梦killaura03
                event_data["clicked_players"].append(clientApi.GetLocalPlayerId())
            self.original_NotifyToServer(event_name, event_data)
        Zmeng.NotifyToServer = NotifyToServer

    def OnDisable(self):
        Zmeng = clientApi.GetSystem("AntiCheatingMod", "AntiCheatingClientSystem")
        if not Zmeng and not self.original_NotifyToServer:
            return True
        Zmeng.NotifyToServer = self.original_NotifyToServer

    def Execute(self, label, args): #type: (str, list[str]) -> None
        if len(args) > 0:
            self.Message = args[0].lower() == "true"
            Api.Message("§cC§eh§ar§bMod §7>> §r修改成功!")
        else:
            return False
