# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
import Client
import math

Config = clientApi.GetEngineCompFactory().CreateConfigClient(clientApi.GetLevelId())

def loadConfig(file = 'default'):
    dict = Config.GetConfigData('/chrmod/' + file + '.json', True)
    Client.instance.prefix = dict.get('prefix', '.')
    for module in Client.instance.Modules:
        cfg = dict.get(module.name, {'open': module.open, 'key': module.key})
        for key, value in cfg.items():
            if key == 'open':
                module.open = cfg['open']
            elif key == 'key':
                module.key = cfg['key']
            else:
                module.args[key] = value
        if module.open: #初始化
            module.func(module)

def saveConfig(file = 'default'):
    dict = {
        'prefix': Client.instance.prefix
    }
    for module in Client.instance.Modules:
        cfg = dict[module.name] = {'open': module.open, 'key': module.key}
        for key, value in module.args.items():
            if key == 'args':
                cfg[key] = value
    return Config.SetConfigData('/chrmod/' + file + '.json', dict, True)

def isExists(file = 'default'):
    return not Config.GetConfigData('/chrmod/' + file + '.json', True) == { }
    