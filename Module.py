# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
import Client
import Api

class Module(object):
    def __init__(self, name, func, key='.', open=False, desc='', message='§cC§eh§ar§bMod §7>> §r{module} {status}', type=0, sound='note.hat', **args):
        #type: (str, function, str, bool, str, str, int, str, any) -> Module
        ''' 参数2的function有一个module，是功能 type: 0开，关 1按下，弹起 2始终关闭 '''
        self.name = name
        self.func = func
        self.key = key
        self.open = open
        self.desc = desc
        self.message = message
        self.type = type
        self.sound = sound
        self.args = args

def Sprint(module):
    if module.open:
        Api.SendMessage('§a自动疾跑已开启 §7(Key: I)')
    else:
        Api.SendMessage('§c自动疾跑已关闭 §7(Key: I)')
    Client.instance.sprint = module.open

def Zoom(module):
    CameraComp = clientApi.GetEngineCompFactory().CreateCamera(clientApi.GetLocalPlayerId())
    if module.open:
        Client.instance.fov = CameraComp.GetFov()
        CameraComp.SetFov(30.0)
        Api.SendMessage('§rFov: 30.0')
    else:
        CameraComp.SetFov(Client.instance.fov)
        Api.SendMessage('§rFov: ' + str(Client.instance.fov))

def List(module):
    Api.SendMessage('§cC§eh§ar§bMod §7>> 玩家列表:')
    for playerId in Api.GetPlayerList():
        x, y, z = clientApi.GetEngineCompFactory().CreatePos(playerId).GetPos()
        Api.SendMessage('§cC§eh§ar§bMod §7>> ' + str(clientApi.GetEngineCompFactory().CreateName(playerId).GetName()) + ' Position: (' + str(int(x)) + ', ' + str(int(y)) + ', ' + str(int(z)) + ')')

def Closest(module):
    player, Distance = Api.GetClosestPlayer(clientApi.GetLocalPlayerId())
    Api.SendMessage('§cC§eh§ar§bMod §7>> §r距离你最近的玩家: ' + str(clientApi.GetEngineCompFactory().CreateName(player).GetName()) + ', 距离: ' + str(Distance))

def Aimbot(module):
    GameComp = clientApi.GetEngineCompFactory().CreateGame(clientApi.GetLocalPlayerId())
    if module.open and module.args.get('timer', None) == None:
        module.args['timer'] = GameComp.AddRepeatedTimer(0.005, AutoAiming_Func)
    else:
        GameComp.CancelTimer(module.args.get('timer', None))
        module.args['timer'] = None

def AutoAiming_Func():
    minPos = ()
    if Client.instance.entity != '':
        entity = Client.instance.entity
        player, Distance = Api.GetClosestPlayer(clientApi.GetLocalPlayerId())
        if player != -2:
            entity = player
        strlang = len(str(entity))
        if strlang > 5 and entity != clientApi.GetLocalPlayerId():
            minPos = clientApi.GetEngineCompFactory().CreatePos(entity).GetPos()
            clientApi.GetEngineCompFactory().CreateRot(clientApi.GetLocalPlayerId()).SetPlayerLookAtPos(minPos, 150, 150, True)	

def RemoteShop(module):
    system = clientApi.GetSystem('HYTShopMod', 'HYTShopModClientSystem')
    if system == None:
        Api.SendMessage('§cC§eh§ar§bMod §7>> §rMod不存在!')
        return
    system.openShop({ })
    Api.SendMessage('§cC§eh§ar§bMod §7>> §r商店已打开 (花雨庭模式)')

def Disabler(module):
    if len(module.args.get('args', [])) > 0: 
        module.open = not module.open
        module.args['message'] = module.args['args'][0].lower() == 'true'
        Api.SendMessage('§cC§eh§ar§bMod §7>> §r修改完毕!')
        return
    Zmeng = clientApi.GetSystem("AntiCheatingMod", "AntiCheatingClientSystem")
    if not Zmeng: 
        module.open = False
        return
    if module.open:
        global original_NotifyToServer 
        original_NotifyToServer = Zmeng.NotifyToServer
        def NotifyToServer(event_name, event_data):
            if event_name == "KickSelf": #绕过逐梦踢出自己
                if module.args.get('message', True):
                    Api.SendMessage('§cC§eh§ar§bMod §7>> §r逐梦启元尝试踢出你，因为 ' + event_data['reason'])
                return
            if event_name == "Ping": #绕过逐梦killaura03
                event_data["clicked_players"] = [clientApi.GetLocalPlayerId()]
            original_NotifyToServer(event_name, event_data)
        Zmeng.NotifyToServer = NotifyToServer
    else:
        Zmeng = clientApi.GetSystem("AntiCheatingMod", "AntiCheatingClientSystem")
        Zmeng.NotifyToServer = original_NotifyToServer

def Flight(module):
    if len(module.args.get('args', [])) > 0: 
        try:
            module.args['speed'] = float(module.args['args'][0])
        except:
            Api.SendMessage('§cC§eh§ar§bMod §7>> §r参数错误!')
        Api.SendMessage('§cC§eh§ar§bMod §7>> §r修改完毕!')
        return
    GameComp = clientApi.GetEngineCompFactory().CreateGame(clientApi.GetLocalPlayerId())
    if module.open and module.args.get('timer', None) == None:
        module.args['timer'] = GameComp.AddRepeatedTimer(0.01, Flight_Func, module.args.get('speed', 1))
    else:
        GameComp.CancelTimer(module.args.get('timer', None))
        module.args['timer'] = None

def Flight_Func(flightSpeed = 1):
    PlayerComp = clientApi.GetEngineCompFactory().CreatePlayer(clientApi.GetLocalPlayerId())
    yrot , xrot = clientApi.GetEngineCompFactory().CreateRot(clientApi.GetLocalPlayerId()).GetRot()
    x, z = 0, 0
    if PlayerComp.isSneaking():
        ym = -1 * flightSpeed
    elif Client.instance.jump:
        ym = 1 * flightSpeed
    else:
        ym = 0.002
    if Client.instance.downkey.get('87', False):
        x, y, z = clientApi.GetDirFromRot((6 , xrot))
    if Client.instance.downkey.get('65', False):
        x, y, z = clientApi.GetDirFromRot((6 , xrot - 83.55))
    if Client.instance.downkey.get('83', False):
        x, y, z = clientApi.GetDirFromRot((6 , xrot - 180))
    if Client.instance.downkey.get('68', False):
        x, y, z = clientApi.GetDirFromRot((6 , xrot + 83.55))
    if Client.instance.downkey.get('87', False) and Client.instance.downkey.get('65', False):
        x, y, z = clientApi.GetDirFromRot((6 , xrot - 41.755))
    if Client.instance.downkey.get('87', False) and Client.instance.downkey.get('68', False):
        x, y, z = clientApi.GetDirFromRot((6 , xrot + 41.755))
    if Client.instance.downkey.get('83', False) and Client.instance.downkey.get('65', False):
        x, y, z = clientApi.GetDirFromRot((6 , xrot + 221.775))
    if Client.instance.downkey.get('83', False) and Client.instance.downkey.get('68', False):
        x, y, z = clientApi.GetDirFromRot((6 , xrot - 221.775))
    clientApi.GetEngineCompFactory().CreateActorMotion(clientApi.GetLocalPlayerId()).SetMotion((x * flightSpeed , ym , z * flightSpeed))

def Popup(module):
    Client.instance.popup = module.open

def Spammer(module):
    GameComp = clientApi.GetEngineCompFactory().CreateGame(clientApi.GetLocalPlayerId())
    if len(module.args.get('args', [])) > 0: 
        module.open = False
        try:
            module.args['message'] = module.args['args'][0]
            module.args['delay'] = float(module.args['args'][1])
            iength = int(module.args['args'][2])
            module.args['length'] = iength if iength > 0 else 0
            Api.SendMessage('§cC§eh§ar§bMod §7>> §r修改完毕!')
            GameComp.CancelTimer(module.args.get('timer', None))
            module.args['timer'] = None
            Client.instance.OpenModule(module, True, [])
        except:
            Api.SendMessage('§cC§eh§ar§bMod §7>> §r参数错误!')
        return
    if module.open and module.args.get('timer', None) == None:
        module.args['timer'] = GameComp.AddRepeatedTimer(module.args.get('delay', 1), Spammer_Func, module.args.get('message', 'ChrMod bypass ZMQY!'), module.args.get('length', 8))
    else:
        GameComp.CancelTimer(module.args.get('timer', None))
        module.args['timer'] = None

def Spammer_Func(text, length):
    Api.SendChatMsg(text + (' | ' + Api.GetRandomText(length) if length > 0 else ''))

def TPAura(module):
    GameComp = clientApi.GetEngineCompFactory().CreateGame(clientApi.GetLocalPlayerId())
    if module.open and module.args.get('timer', None) == None:
        module.args['timer'] = GameComp.AddRepeatedTimer(0.001, TPAura_Func)
    else:
        GameComp.CancelTimer(module.args.get('timer', None))
        module.args['timer'] = None

def TPAura_Func():
    #for i in range(128):
        if Client.instance.range > 359.0:
            Client.instance.range = 0.0
        Client.instance.range += 0.2
        range2 = Client.instance.range
        myPos = clientApi.GetEngineCompFactory().CreatePos(clientApi.GetLocalPlayerId()).GetPos()
        nePos = ()
        entity = Client.instance.entity
        player, Distance = Api.GetClosestPlayer(clientApi.GetLocalPlayerId())
        if player != -2:
            entity = player
        strlang= len(str(entity))
        if strlang > 5 and entity != clientApi.GetLocalPlayerId():
            x, y, z = clientApi.GetEngineCompFactory().CreatePos(entity).GetPos()
            nePos_x , nePos_z = Api.GetCirclePos(x, z, 2, range2)
            nePos = (nePos_x, y, nePos_z)
            mPos = Api.MotionPosCountYadd(nePos, myPos, 0.0)
            nPos = Api.MotionPosRectify(mPos)
            clientApi.GetEngineCompFactory().CreateActorMotion(clientApi.GetLocalPlayerId()).SetMotion(nPos)

def HighJump(module):
    if len(module.args.get('args', [])) > 0: 
        module.open = not module.open
        try:
            Client.instance.hjvalue = float(module.args['args'][0])
        except:
            Api.SendMessage('§cC§eh§ar§bMod §7>> §r参数错误!')
        return
    Client.instance.highjump = module.open