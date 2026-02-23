# -*- coding: utf-8 -*-

from ..registry import Command
from ...module import manager
from ...api.client import DisplayClientMessage

class Modules(Command):
    def __init__(self):
        Command.__init__(self, 'modules', '模块列表。', '.modules', [])

    def Execute(self, args):
        DisplayClientMessage('§b模块列表')
        
        types = manager.GetManager().GetModuleTypes()
        for category in types: # type: ignore
            DisplayClientMessage('§r{}'.format(category))

            for module in types[category]: # type: ignore
                DisplayClientMessage('§7{} - {}'.format(module.name, module.description))

        return True