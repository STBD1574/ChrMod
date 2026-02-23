# -*- coding: utf-8 -*-
#v3主要是彻底重写了module，之前的太难看了

import mod.client.extraClientApi as clientApi
import ChrMod.Api as Api

modules = [] #type: list[Module]

class ModuleType:
    COMBAT = "Combat"
    MOVEMENT = "Movement"
    MISC = "Misc"
    VISUAL = "Visual"

class Module:
    def __init__(self, name, description, group="Misc", open=False, key="", type=0, usageMessage="", **args):
        self.name = name #type: str
        self.description = description #type: str
        self.group = group #type: str
        self.open = open #type: str
        self.key = key #type: str
        self.type = type #type: int # 0是按下开关，1是点击开关（按下开，弹起关），2是始终开启（只有开启）
        self.usageMessage = usageMessage #type: str
        self.args = args #type: dict[str, any]

    def OnEnable(self): #type: () -> None | bool
        ''' 返回True代表取消开启 '''
        pass

    def OnDisable(self): #type: () -> None | bool
        ''' 返回True代表取消关闭 '''
        pass

    def Execute(self, label, args): #type: (str, list[str]) -> None | bool
        ''' 当给予参数时，调用该方法 '''
        pass
    
    def Update(self):
        ''' 客户端每帧调用，一秒有三十帧 '''
        pass

def InitModules():
    # 先要定义好module类，再导入所有的模块。
    from ChrMod.Module.Combat.Aimbot import Aimbot
    from ChrMod.Module.Combat.Reach import Reach
    from ChrMod.Module.Combat.Killaura import Killaura
    from ChrMod.Module.Combat.TPAura import TPAura
    from ChrMod.Module.Movement.Fly import Fly
    from ChrMod.Module.Movement.AntiVoid import AntiVoid
    from ChrMod.Module.Movement.HighJump import HighJump
    from ChrMod.Module.Movement.ClickTP import ClickTP
    from ChrMod.Module.Movement.Blink import Blink
    from ChrMod.Module.Misc.Invisibility import Invisibility
    from ChrMod.Module.Misc.RpcLogger import RpcLogger
    from ChrMod.Module.Misc.Spammer import Spammer
    from ChrMod.Module.Misc.Disabler import Disabler
    from ChrMod.Module.Misc.RemoteShop import RemoteShop
    from ChrMod.Module.Misc.List import List
    from ChrMod.Module.Visual.Zoom import Zoom
    from ChrMod.Module.Visual.Popup import Popup
    from ChrMod.Module.Visual.HudTip import HudTip
    from ChrMod.Module.Visual.ShowHealth import ShowHealth
    from ChrMod.Module.Visual.ClickGui import ClickGui
    #Combat
    modules.append(Aimbot())
    modules.append(Reach())
    modules.append(Killaura())
    modules.append(TPAura())
    #Movement
    modules.append(Fly())
    modules.append(AntiVoid())
    modules.append(HighJump())
    modules.append(ClickTP())
    modules.append(Blink())
    #Misc
    modules.append(Invisibility())
    modules.append(RpcLogger())
    modules.append(Spammer())
    modules.append(Disabler())
    modules.append(RemoteShop())
    modules.append(List())
    #Visual
    modules.append(Zoom())
    modules.append(Popup())
    modules.append(HudTip())
    modules.append(ShowHealth())
    modules.append(ClickGui())

def UpdateModules():
    for module in modules:
        module.Update()

def ChangeModuleState(module, open, args={ }, isKey=False): #type: (Module, bool, dict[str, any], bool) -> None
    module.args.update(args)
    if not (module.OnEnable if open else module.OnDisable)() == True:
        module.open = open
        if isKey and (open or module.type == 1):
            Api.PlayMusic("random.click", entityId=clientApi.GetLocalPlayerId())
        Api.Message("§cC§eh§ar§bMod §7>> §r" + module.name + (" Enabled ■" if open else " Disabled □"))

def ModuleExecute(module, label, args): #type: (Module, str, list[str]) -> None
    if module.Execute(label, args) == False:
        Api.Message("§cC§eh§ar§bMod §7>> §r用法: " + module.usageMessage)

def GetModuleTypes(): #type: () -> dict[str, list[Module]]
    types = { } #type: dict[str, list[Module]]
    for module in modules:
        if module.group in types:
            types[module.group].append(module)
        else:
            types[module.group] = [module]
    return types

def GetModule(name): #type: (str) -> Module | None
    for module in modules:
        if module.name == name:
            return module
    return None