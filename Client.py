# -*- coding: utf-8 -*-
#送反编译源代码的人的几句话:
#看你妈的代码，反编译是吧，我就操你妈。我他妈筷子水泥，捅进你妈逼里。我告诉你，你就是个畜生，只会反编译的畜生。
#操你妈的还看是吧，傻逼，我祝你祖宗十八代全部死光。
#傻逼还看是吧？我送你个网站：madou.club，祝你一辈子死在这不出来。
import mod.client.extraClientApi as clientApi
import Listener as Listener
import Api
import Config as Config
import Module as ModuleFunc
import Command as CommandFunc
from mod_log import logger as logger
import utility
import json
from python_tools import instance as python_tools

ClientSystem = clientApi.GetClientSystemCls()
ListenerFactory = Listener.ListenerFactory()
EngineListener = ListenerFactory.CreateListener(namespace = 'Minecraft', systemName = 'Engine')
Listen = ListenerFactory.CreateListenerProxy()

@Listen()
class Main(ClientSystem):
    def __init__(self, namespace, systemName):
        ClientSystem.__init__(self, namespace, systemName)
        global instance
        instance = self
        Module = ModuleFunc.Module
        Command = CommandFunc.Command

        #Varables
        self.GameComp = clientApi.GetEngineCompFactory().CreateGame(clientApi.GetLocalPlayerId())
        self.Modules = [
            Module('AutoSprint', ModuleFunc.Sprint, '73', True, '自动疾跑。', None),
            Module('Zoom', ModuleFunc.Zoom, '67', False, '放大器。', None, 1),
            Module('List', ModuleFunc.List, '9', False, '获取玩家列表。', None, 2),
            Module('Closest', ModuleFunc.Closest, '188', False, '获取距离最近的玩家。', None, 2),
            Module('Aimbot', ModuleFunc.Aimbot, '190', False, '自动瞄准。'),
            Module('RemoteShop', ModuleFunc.RemoteShop, '192', False, '远程商店 (花雨庭)。', None, 2),
            Module('Disabler', ModuleFunc.Disabler, '36', True, '绕过某些反作弊的检测。 [message: bool]'),
            Module('Flight', ModuleFunc.Flight, '35', False, '动量飞行。 [speed: float]'),
            Module('Popup', ModuleFunc.Popup, '.',  False, '设置Popup状态栏的显示。'),
            Module('Spammer', ModuleFunc.Spammer, '33', False, '自动发送消息 (以秒为单位)。 [message: str] [delay: float] [length: int]'),
            Module('TPAura', ModuleFunc.TPAura, '34', False, '对玩家环绕。'),
            Module('HighJump', ModuleFunc.HighJump, '.', False, '高跳。 [high: flaot]')
        ]
        self.Commands = [
            Command('help', CommandFunc.HelpCommand, '获取帮助。'),
            Command('inputmode', CommandFunc.InputModeCommand, '修改操作方式。 <inputMode: int> [type: bool]'),
            Command('platform', CommandFunc.PlatformCommand, '修改运行平台。 <platform: int>'),
            Command('execute', CommandFunc.ExecuteCommand, '运行Python代码 (exec)，\\n为换行。 <execute...: string>'),
            Command('size', CommandFunc.SizeCommand, '修改主窗口的大小。 <x: int> <y: int>'),
            Command('rejoin', CommandFunc.RejoinCommand, '重新加入本地游戏 (服务器无效)。'),
            Command('bind', CommandFunc.BindCommand, '绑定模块的快捷键 (设置None为解绑)。 <module: string> <key: string>'),
            Command('listenevent', CommandFunc.ListenEventCommand, '监听指定system的事件。 <namespace: string> <systemName: string> <eventName: string> [isUnListen: bool]'),
            Command('config', CommandFunc.ConfigCommand, '配置管理器。 <type(save, load): string> <file: string>'),
            Command('rpclogger', CommandFunc.RpcLoggerCommand, '向指定的system置入记录器 (不是我不想做全局，是真不行啊)。 <namespace: string> <systemName: string>')
        ]

        self.fov = 0
        self.tick = 0
        self.debug = False
        self.entity = -2 #为了兼容性
        self.sprint = True
        self.range = 0.0 #range放这的原因是，别的文件无法定义变量。。。
        self.timer = None
        self.jump = False
        self.highjump = False
        self.hjvalue = 1.2
        self.downkey = { }
        self.popup = False
        self.prefix = '.'

        clientApi.GetPlatform = lambda : 1 #platform修改
        CommandFunc.InputModeCommand([2]) #inputmode修改
        clientApi.GetEngineCompFactory().CreateOperation(clientApi.GetLocalPlayerId()).SetHoldTimeThreshold(200) #hytmod遗留
        clientApi.GetEngineCompFactory().CreatePlayer(clientApi.GetLocalPlayerId()).ClosePlayerHitBlockDetection()
        clientApi.GetEngineCompFactory().CreatePlayer(clientApi.GetLocalPlayerId()).ClosePlayerHitMobDetection()
        clientApi.SetEnableReconnectNetgame(True)

        if not Config.isExists('default'):
            Config.saveConfig('default')
        Config.loadConfig('default')

        system = clientApi.GetSystem('Minecraft', 'chatExtension') #关闭聊天扩展
        if system != None: system.chatExtenOpenStateChange({'open': True})
    
        Api.SendMessage('加载完毕!')
        Api.SendMessage('ChrMod >> 测试MCP加密: ' + utility.encrypt_http_content('Hello World!') + ', 测试屏蔽词: 网易我操你妈')
        exec('Api.SendMessage("ChrMod >> 这是一个由exec函数运行的代码发出的消息")')

    def OpenModule(module, isOpen = True, args = []):
        #type: (ModuleFunc.Module, bool, dict) -> None
        ''' 打开一个模块 '''
        module.open = isOpen
        module.args['args'] = args
        if module.message: 
            Api.SendMessage(module.message.replace('{module}', module.name).replace('{status}', 'Enabled ■' if module.open else 'Disabled □'))
        module.func(module)

    @EngineListener('LoadClientAddonScriptsAfter')
    def ModLoad(self, args):
        #实现rpclogger
        from mod.common.network import defaultrpc as Rpc
        func = Rpc.CServerRpc.ModEventC2S
        def ModEventC2S(namespace, systemName, eventName, eventData):
            import Script.Client as Client
            if Client.instance.debug:
                Api.SendMessage('§cC§eh§ar§bMod §7>> §rModEventC2S: namespace: ' + namespace + ' systemName: ' + systemName + ' eventName: ' + eventName + ' eventData: ' + str(eventData))
            func(namespace, systemName, eventName, eventData)
        Rpc.CServerRpc.ModEventC2S = ModEventC2S

    @EngineListener('ClientJumpButtonPressDownEvent', 'ClientJumpButtonReleaseEvent')
    def PlayerJump(self, args = { }):
        self.jump = not args == { }
        if self.jump and self.highjump:
            args['continueJump'] = False
            clientApi.GetEngineCompFactory().CreateActorMotion(clientApi.GetLocalPlayerId()).SetMotion((0, self.hjvalue, 0))

    @EngineListener('PushScreenEvent')
    def PushScreenEvent(self, args):
        if self.debug:
            Api.SendMessage('PushScreenEvent: ' + str(args))

    @EngineListener('UiInitFinished')
    def UiInitFinished(self, args):
        Api.SendMessage('ChrMod - V2')
        Api.SendMessage('Uid: ' + str(clientApi.GetEngineCompFactory().CreatePlayer(-2).getUid()))
        ip, port = clientApi.GetLocalAreaServerAndIp()
        Api.SendMessage('LocalIP: ' + str(clientApi.GetIP()) + ' ServerIP: ' + str(str(ip)) + ' ServerPort: ' + str(port))
        Api.SendMessage('作者: Eison, 欢迎你的使用!')

    @EngineListener('OnScriptTickClient')
    def ScriptTick(self):
        self.tick += 1
        clientApi.GetEngineCompFactory().CreateOperation(clientApi.GetLocalPlayerId()).SetCanAll(True) #解锁客户端带来的限制，没人管得住我
        if self.tick % 3 == 0:
            self.entity = clientApi.GetEngineCompFactory().CreateCamera(clientApi.GetLocalPlayerId()).GetChosenEntity()
            if self.popup:
                self.GameComp.SetTipMessage('InputMode: ' + str(clientApi.GetEngineCompFactory().CreatePlayerView(clientApi.GetLevelId()).GetToggleOption('INPUT_MODE') + 1) + ' Platform: ' + str(clientApi.GetPlatform()) + ' FPS: ' + str(int(self.GameComp.GetFps())))

    @EngineListener('ClickChatSendClientEvent') #实际上ClientChatEvent在服务器环境是无效的
    def ChatCommand(self, args): #cancel=bool, message=str
        if self.debug:
            Api.SendMessage('ClientChatEvent: ' + str(args))
        if args['message'][0] == self.prefix:
            args['cancel'] = True
        else:
            args['cancel'] = False
            return
        length = len(self.prefix)
        name = args['message'][length:].split(' ')[0]
        args = Api.list_remove_empty(args['message'][length:].split(' ')[length:])
        for module in self.Modules:
            if module.name.lower() == name.lower():
                self.OpenModule(module, not module.open, args)
                return
        for cmd in self.Commands:
            if cmd.name.lower() == name.lower():
                if cmd.func(args) == False: 
                    Api.SendMessage('§cC§eh§ar§bMod §7>> §r参数错误!')
                return
        Api.SendMessage('§cC§eh§ar§bMod §7>> §r不存在的命令: ' + name + ', 请检查输入!')

    @EngineListener('OnKeyPressInGame')
    def OnPressKey(self, args):
        if args['screenName'] != 'hud_screen' and (args['key'] != '27' or args['key'] != '35'): return
        MotionComp = clientApi.GetEngineCompFactory().CreateActorMotion(clientApi.GetLocalPlayerId())
        for module in self.Modules:
            module.args['args'] = []
            if module.key == args['key']:
                if args['isDown'] == '1':
                    Api.PlaySound(module.sound, clientApi.GetLocalPlayerId())
                    self.OpenModule(module, module.open == False if module.type == 0 or module.type == 1 else False, [])
                if args['isDown'] == '0':
                    if module.type == 1:
                        Api.PlaySound(module.sound, clientApi.GetLocalPlayerId())
                        self.OpenModule(module, False, [])
        if args['isDown'] == '1':
            self.downkey[args['key']] = True
            if args['key'] == '87' and self.sprint: #自动疾跑
                MotionComp.BeginSprinting()
            if args['key'] == '27': #关闭Ui
                clientApi.PopTopUI()
                clientApi.GetTopUINode().SetRemove()
                system = clientApi.GetSystem('HYTShopMod', 'HYTShopModClientSystem') #花雨庭操作
                if system: system.ShopCloseEvent({ })
        if args['isDown'] == '0':
            self.downkey[args['key']] = False
            if args['key'] == '87' and self.sprint:
                MotionComp.EndSprinting()

    def OnEvent(self, args = { }):
        Api.SendMessage('§cC§eh§ar§bMod §7>> §rOnEvent: ' + json.dumps(args, encoding = 'utf-8', ensure_ascii = False))

# if args['key'] == '36':  被注释掉的代码（悲）
#     self.count += 1
#     if self.count > 20:
#         self.ListenForEvent('HYTShopMod', 'HYTShopModServerSystem', 'ShopOpenEvent', self, lambda args = { } : Api.SendMessage('§cC§eh§ar§bMod §7>> §rOpenShop ' + str(args)))
#         self.ListenForEvent('HYTShopMod', 'HYTShopModServerSystem', 'ShopCloseEvent', self, lambda args = { } : Api.SendMessage('§cC§eh§ar§bMod §7>> §rCloseShop ' + str(args)))
#         self.ListenForEvent('HYTShopMod', 'HYTShopModServerSystem', 'BuyGoodEvent', self, lambda args = { } : Api.SendMessage('§cC§eh§ar§bMod §7>> §rBuyGood ' + str(args)))
#         self.ListenForEvent('HYTShopMod', 'HYTShopModServerSystem', 'RefreshPlayerCurrency', self, lambda args = { } : Api.SendMessage('§cC§eh§ar§bMod §7>> §rRefreshCurrency ' + str(args)))
#         self.ListenForEvent('HYTShopMod', 'HYTShopModServerSystem', 'RefreshShopGoods', self, self, lambda args = { } : Api.SendMessage('§cC§eh§ar§bMod §7>> §rRefreshGoods ' + str(args)))
#         if self.count % 2 == 1:
#             self.debug = True
#         else:
#             self.debug = False