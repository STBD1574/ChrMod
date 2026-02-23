# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
from ChrMod.Command.CommandManager import Command
import ChrMod.Api as Api
from ChrMod.Client import instance as Client

class Teleport(Command):
    def __init__(self):
        Command.__init__(self, "teleport", "传送至指定地点或玩家。", ".teleport <x> <y> <z> 或 .teleport <player>", ["tp"])

    def Execute(self, label, args):
        try:
            px, py, pz = Api.Entity.GetPosition(clientApi.GetLocalPlayerId())
            x = (px + float(args[0][1:]) if len(args[0]) > 1 else px) if args[0][0] == '~' else float(args[0]) #相对坐标算法
            y = (py + float(args[1][1:]) if len(args[1]) > 1 else py) if args[1][0] == '~' else float(args[1])
            z = (pz + float(args[2][1:]) if len(args[2]) > 1 else pz) if args[2][0] == '~' else float(args[2])
            Api.Message('§cC§eh§ar§bMod §7>> §r传送' + ('成功' if Api.Teleport((x, y, z)) else '失败'))
            return True
        except:
            try:
                name = args[0][1:].replace('\"', '') if args[0][0] == '@' else args[0]
                for playerId in Api.GetPlayerList():
                    if str(Api.Entity.GetName(playerId, False)) == name:
                        Api.Teleport(Api.Entity.GetPosition(playerId))
                        Api.Message('§cC§eh§ar§bMod §7>> §r已传送至 ' + name)
                        return True
            except:
                if Client.mCurrentEntity != 0:
                    x, y, z = Api.Entity.GetPosition(Client.mCurrentEntity)
                    Api.Teleport((x, y, z))
                    Api.Message('§cC§eh§ar§bMod §7>> §r已传送至 ' + Api.Entity.GetName(Client.mCurrentEntity))
                    return True
        return False