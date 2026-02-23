# -*- coding: utf-8 -*-
# author Eison
# 2024/07/14

from collections import defaultdict
from .module import Module

class Manager: 
    def __init__(self):
        self.modules = { } # type: dict[str, Module]

    def AddModule(self, module): # type: (Module) -> None
        self.modules[module.name.lower()] = module

    def DeleteModule(self, name): # type: (str) -> bool
        lowerName = name.lower()
        if lowerName in self.modules:
            del self.modules[lowerName]
            return True
        return False

    def GetModule(self, nameOrType): # type: (str | type[Module]) -> Module | None
        if isinstance(nameOrType, str):
            lowerName = nameOrType.lower()
            if lowerName in self.modules:
                return self.modules[lowerName]
        elif isinstance(nameOrType, type) and issubclass(nameOrType, Module):
            for module in self.modules.itervalues():
                if isinstance(module, nameOrType):
                    return module

        return None

    def GetModuleTypes(self): # type: () -> dict[str, list[Module]]
        types = defaultdict(list)
        for module in self.modules.itervalues():
            types[module.category].append(module)
        return dict(types)

manager = Manager()

def GetManager(): # type: () -> Manager
    return manager

def InitModules(): # type: () -> None
    from combat.aimbot import Aimbot
    from combat.killaura import Killaura
    from combat.reach import Reach
    from combat.tp_aura import TPAura
    from combat.velocity import Velocity
    from misc.disabler import Disabler
    from misc.py_rpc_logger import PyRpcLogger
    from misc.spammer import Spammer
    from misc.crasher import Crasher
    from movement.click_tp import ClickTP
    from movement.fly import Fly
    from movement.high_jump import HighJump
    from movement.respawn import Respawn
    from movement.bunny_hop import BunnyHop
    from movement.boat_fly import BoatFly
    from visual.click_gui import ClickGui
    from visual.esp import ESP
    from visual.hud_tip import HudTip
    from visual.show_health import ShowHealth
    from visual.coordinates import Coordinates
    from visual.name_tag import NameTag
    manager.AddModule(Aimbot())
    manager.AddModule(Killaura())
    manager.AddModule(Reach())
    manager.AddModule(TPAura())
    manager.AddModule(Velocity())
    manager.AddModule(Disabler())
    manager.AddModule(PyRpcLogger())
    manager.AddModule(Spammer())
    manager.AddModule(Crasher())
    manager.AddModule(ClickTP())
    manager.AddModule(Fly())
    manager.AddModule(HighJump())
    manager.AddModule(Respawn())
    manager.AddModule(BunnyHop())
    manager.AddModule(BoatFly())
    manager.AddModule(ClickGui())
    manager.AddModule(ESP())
    manager.AddModule(HudTip())
    manager.AddModule(ShowHealth())
    manager.AddModule(Coordinates())
    manager.AddModule(NameTag())