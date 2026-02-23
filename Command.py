# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
from mod.common.minecraftEnum import KeyBoardType
import Client
import Config
import Api
import traceback
import json

class Command(object):
    def __init__(self, name, func, desc='Not descption.', **args):
        #type: (str, function, str, any) -> Command
        ''' 参数3的function有一个str列表，是参数 '''
        self.name = name
        self.desc = desc
        self.func = func
        self.args = args

def HelpCommand(args):
    Api.SendMessage('§b命令帮助:\n§r模块:')  
    for module in Client.instance.Modules:
        Api.SendMessage('§7' + module.name + ' - §o' + module.desc)
    Api.SendMessage('§r命令:')
    for cmd in Client.instance.Commands:
        Api.SendMessage('§7' + cmd.name + ' - §o' + cmd.desc)
    return True

def InputModeCommand(args):
    if len(args) < 1: return False
    mode = 0
    type = False
    if len(args) > 1:
        type = args[1].lower() == 'true'
    try:
        mode = (int(args[0]))
    except:
        return False
    if type:
        clientApi.SetInputMode(mode)
    else:
        func = clientApi.GetEngineCompFactory().CreatePlayerView(clientApi.GetLevelId()).GetToggleOption
        def GetToggleOption(optionId):
            if optionId == 'INPUT_MODE': 
                return mode
            func(optionId)
        clientApi.GetEngineCompFactory().CreatePlayerView(clientApi.GetLevelId()).GetToggleOption = GetToggleOption
    Api.SendMessage('§cC§eh§ar§bMod §7>> §r修改完毕!')  
    return True   

def PlatformCommand(args):
    if len(args) < 1: return False
    platform = clientApi.GetPlatform()
    try:
        platform = int(args[0])
    except:
        return False
    clientApi.GetPlatform = lambda : platform
    Api.SendMessage('§cC§eh§ar§bMod §7>> §r修改完毕!')  
    return True

def ExecuteCommand(args):
    if len(args) < 1: return False
    cmd = ''
    for i in args:
        cmd += i + ' '
    try:
        exec(cmd.replace('\\n', '\n'))
    except:
        Api.SendMessage('§cC§eh§ar§bMod §7>> §r运行出错! ' + traceback.format_exc())
    return True

def SizeCommand(args):
    if len(args) < 2: return False
    x, y = 0, 0
    try:
        x = int(args[0])
        y = int(args[1])
    except:
        return False
    clientApi.SetMainWindowSize(x, y)
    return True

def RejoinCommand(args):
    clientApi.RestartLocalGame()
    return True

def BindCommand(args):
    if len(args) < 2: return False
    if args[1].lower() == 'none':
        Api.SendMessage('§cC§eh§ar§bMod §7>> §r设置为空成功!')  
        return True
    else:
        for module in Client.instance.Modules:
            if module.name.lower() == args[0].lower():
                if args[1].lower() == 'none':
                    module.key = '.'
                    return True
                else:
                    key = module.key
                    try:
                        key = ord(args[1][0].lower())
                        Api.SendMessage('§cC§eh§ar§bMod §7>> §r设置成功!')  
                    except:
                        for type in dir(KeyBoardType):
                            if type[4:].lower() == args[1].lower():
                                key = type
                                Api.SendMessage('§cC§eh§ar§bMod §7>> §r设置成功!')  
                                break
                    module.key = key    
                    return True
    return False

def ListenEventCommand(args):
    if len(args) < 3: return False
    isUnListen = args[3].lower() == 'true' if len(args) > 3 else False
    if not isUnListen:
        func = Client.instance.ListenForEvent
    else:
        func = Client.instance.UnListenForEvent
    for event in args[2].split(','):
        func(args[0], args[1], event, Client.instance, Client.instance.OnEvent)
        Api.SendMessage('§cC§eh§ar§bMod §7>> §r' + ('取消' if isUnListen else '开始') + '监听事件 namespace: ' + args[0] + ' systemName: ' + args[1] + ' eventName: ' + event) 
    return True

def ConfigCommand(args):
    if len(args) < 2: return False
    if args[0].lower() == 'load':
        Config.loadConfig(args[1])
    elif args[0].lower() == 'save':
        Config.saveConfig(args[1])
    else:
        return False
    return True

def RpcLoggerCommand(args):
    if len(args) < 2: return False
    system = clientApi.GetSystem(args[0], args[1])
    if not system: return False
    with open('rpclogger.txt', 'a', encoding = 'utf-8') as file: pass
    original_NotifyToServer  = system.NotifyToServer
    def NotifyToServer(eventName, eventData):
        Api.SendMessage('§cC§eh§ar§bMod §7>> §rRpcLogger eventName: ' + eventName + ' eventData: ' + json.dumps(eventData, encoding = 'utf-8', ensure_ascii = False))
        file.write('================================\neventName: ' + eventName + ' eventData: ' + json.dumps(eventData, encoding = 'utf-8', ensure_ascii = False))
        original_NotifyToServer(eventName, eventData)
    system.NotifyToServer = NotifyToServer
    Api.SendMessage('§cC§eh§ar§bMod §7>> §r置入RpcLogger成功!')
    return True