# -*- coding: utf-8 -*-

from ..registry import Command
from ...module import manager
from ...api import client

KEYS = {'Y': 89, 'PG_DOWN': 34, 'LBRACKET': 219, 'MULTIPLY': 106, 'SUBTRACT': 109, 'MINUS': 189, '0': 48, '4': 52, 'TAB': 9, '8': 56, 'D': 68, 'H': 72, 'L': 76, 'P': 80, 'T': 84, 'SLASH': 191, 'SCAPE': 27, 'X': 88, 'MENU': 18, 'APOSTRAPHE': 222, 'F9': 120, 'DELETE': 46, 'RETURN': 13, 'GOBACK': 4, 'DOWN': 40, 'BACKSPACE': 8, '3': 51, '7': 55, 'C': 67, 'DIVIDE': 111, 'G': 71, 'O': 79, 'MOUSE_Middle': -97, 'S': 83, 'W': 87, 'F12': 123, 'F13': 124, 'F10': 121, 'F11': 122, 'NUMPAD2': 98, 'NUMPAD3': 99, 'NUMPAD0': 96, 'NUMPAD1': 97, 'NUMPAD6': 102, 'NUMPAD7': 103, 'NUMPAD4': 100, 'NUMPAD5': 101, 'NUMPAD8': 104, 'NUMPAD9': 105, 'UP': 38, 'HOME': 36, 'SEMICOLON': 186, 'ND': 35, 'BACKSLASH': 220, '2': 50, '6': 54, 'LEFT': 37, 'B': 66, 'F': 70, 'DECIMAL': 110, 'J': 74, 'N': 78, 'ADD': 107, 'R': 82, 'MOUSE_LEFT': -99, 'NUM_LOCK': 144, 'V': 86, 'PG_UP': 33, 'Z': 90, 'F1': 112, 'F2': 113, 'F3': 114, 'F4': 115, 'F5': 116, 'F6': 117, 'F7': 118, 'F8': 119, 'QUALS': 187, 'CAPS_LOCK': 20, 'LSHIFT': 16, 'CONTROL': 17, 'INSERT': 45, '1': 49, '5': 53, '9': 57, 'GRAVE': 192, 'A': 65, 'PAUSE': 19, 'SPACE': 32, 'I': 73, 'M': 77, 'PERIOD': 190, 'Q': 81, 'U': 85, 'MOUSE_RIGHT': -98, 'RIGHT': 39, 'RBRACKET': 221, 'COMMA': 188, 'SCROLL': 145}

class Bind(Command):
    def __init__(self):
        Command.__init__(self, 'bind', '绑定模块的快捷键。', '.bind <module> <key>', [])

    def Execute(self, args):
        if len(args) < 1:
            return not client.DisplayClientMessage('{}参数错误!')
        
        module = manager.GetManager().GetModule(args[0])
        if not module:
            return not client.DisplayClientMessage('{}未找到模块 {}.'.format(client.MESSAGE_PREFIX, args[0]))

        if len(args) < 2:
            return not client.DisplayClientMessage('{}模块 {} 的键绑定是 {}， 键代码是 {}'.format(client.MESSAGE_PREFIX, module.name, KEYS.get(module.key, '无'), module.key))
    
        key = args[1] # type: str
        if key not in KEYS:
            return not client.DisplayClientMessage('{}无效的键!')

        if key.isdigit():
            module.key = key
            client.DisplayClientMessage('{}模块 {} 的键绑定已设置为 {}.'.format(client.MESSAGE_PREFIX, module.name, KEYS.get(key, key)))
        else:
            module.key = KEYS[key]
            client.DisplayClientMessage('{}模块 {} 的键绑定已设置为 {}.'.format(client.MESSAGE_PREFIX, module.name, key))

        return True