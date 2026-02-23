# -*- coding: utf-8 -*-

from ..registry import Command
from ...module import manager

class Toggle(Command):
    def __init__(self):
        Command.__init__(self, 'toggle', '设置模块的开关。', '.toggle <module>', {'t'})

    def Execute(self, args): # type: (list[str]) -> bool
        if len(args) < 1:
            return False
        
        for module in manager.GetManager().modules.itervalues():
            if module.name.lower() == args[0].lower():
                module.SetEnabled(not module.GetEnabled())
                return True

        return False