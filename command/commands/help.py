# -*- coding: utf-8 -*-

from ..registry import Command, registry
from ...api.client import DisplayClientMessage

class Help(Command):
    def __init__(self):
        Command.__init__(self, 'help', '获取帮助。', '.help', [])

    def Execute(self, args):
        DisplayClientMessage('§b命令帮助')
        for index in xrange(registry.newIndex): # type: ignore
            command = registry.commands[index]
            DisplayClientMessage('§7{} - {}'.format(command.name, command.description))
        return True