# -*- coding: utf-8 -*-

from ..registry import Command
from ...api import client, modapi
from ... import patch

class Platform(Command):
    def __init__(self):
        Command.__init__(self, 'platform', '设置读取到的设备运行平台。', '.platform <platform> [isRuntime: bool ? hook : runtime]', [ ])

    def Execute(self, args):
        isRuntime = False

        if len(args) > 1:
            isRuntime = args[1] == 'true'
        elif len(args) < 1:
            return False
        
        try:
            if isRuntime:
                modapi.SetPlatform(int(args[0]))
            else:
                patch.setPlatform(int(args[0]))
        except ValueError:
            client.DisplayClientMessage('{}设置失败!'.format(client.MESSAGE_PREFIX))
        finally:
            client.DisplayClientMessage('{}设置成功!'.format(client.MESSAGE_PREFIX))
        
        return True