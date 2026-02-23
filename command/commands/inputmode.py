# -*- coding: utf-8 -*-

from ..registry import Command
from ...api import client
from ... import patch

class InputMode(Command):
    def __init__(self):
        Command.__init__(self, 'inputmode', '设置读取到的操作方式。', '.inputmode <inputmode>', [])

    def Execute(self, args):
        if len(args) < 1:
            return False
        try:
            patch.setInputMode(int(args[0]))
        except ValueError:
            client.DisplayClientMessage('{}设置失败!'.format(client.MESSAGE_PREFIX))
        finally:
            client.DisplayClientMessage('{}设置成功!'.format(client.MESSAGE_PREFIX))
        return True