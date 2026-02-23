# -*- coding: utf-8 -*-
# author Eison
# 2024/07/23

from ..registry import Command
from ...api import client, localplayer, entity

class Teleport(Command):
    def __init__(self):
        Command.__init__(self, 'teleport', '传送到指定位置，支持相对坐标。', '.teleport <x> <y> <z>', {'tp'})

    def Execute(self, args): # type: (list[str]) -> bool
        if len(args) < 3:
            return not client.DisplayClientMessage('§cC§eh§ar§bMod §7>§r 参数错误!')
        
        position = entity.GetPosition(client.GetLocalPlayerId())
        try:
            x = (float(args[0][1:]) if len(args[0]) > 1 else 0) + position[0] if args[0].startswith('~') else float(args[0])
            y = (float(args[1][1:]) if len(args[1]) > 1 else 0) + position[1] if args[1].startswith('~') else float(args[1])
            z = (float(args[2][1:]) if len(args[2]) > 1 else 0) + position[2] if args[2].startswith('~') else float(args[2])
        except ValueError:
            return not client.DisplayClientMessage('§cC§eh§ar§bMod §7>§r 参数错误!')

        localplayer.SetPosition((x, y, z))

        return True