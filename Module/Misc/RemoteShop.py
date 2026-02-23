# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
from ChrMod.Module.ModuleManager import Module, ModuleType
import ChrMod.Api as Api

class RemoteShop(Module):
    def __init__(self):
        Module.__init__(self, "RemoteShop", "远程商店。", ModuleType.MISC, False, None, 2)

    def OnEnable(self):
        HYTShopMod = clientApi.GetSystem("HYTShopMod", "HYTShopModClientSystem")
        if HYTShopMod:
            Api.Message("§cC§eh§ar§bMod §7>> §r远程商店已开启 (花雨庭模式)")
            HYTShopMod.RefreshPlayerCurrency({"currency2": {"item": "minecraft:gold_ingot", "amount": 999, "meta": 0}, "currency3": {"item": "minecraft:diamond", "amount": 999, "meta": 0}, "currency1": {"item": "minecraft:iron_ingot", "amount": 999, "meta": 0}, "currency4": {"item": "minecraft:netherbrick", "amount": 999, "meta": 0}, "currency5": {"item": "minecraft:nether_star", "amount": 999, "meta": 0}})
            HYTShopMod.openShop({ })
        return True #可以隐藏消息