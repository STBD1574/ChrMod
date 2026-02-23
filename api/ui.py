# -*- coding: utf-8 -*-
# author lpCSTR
# 2024/07/16

from ..importer import Module

uiManager   = Module('client.ui.uiManager')
postprocess = Module('postprocess')
game_ruler  = Module('game_ruler')
clientlevel = Module('clientlevel')
gui         = Module('gui')

def RegisterUI(nameSpace, uiKey, clsPath, uiScreenDef=None): # type: (str, str, str, str) -> bool
    if uiScreenDef is None:
        key, clsPath, uinamespace = nameSpace, uiKey, clsPath
        return uiManager.instance().register_ui(key, clsPath, uinamespace)
    else:
        namespace, key, clsPath, uinamespace = nameSpace, uiKey, clsPath, uiScreenDef
        return uiManager.instance().register_ui_new(namespace, key, clsPath, uinamespace)

def CreateUI(nameSpace, uikey=None, createParams=None): # type: (str, str, dict) -> any
    if type(nameSpace) == str and nameSpace != '':
        namespace, uiname, param = nameSpace, uikey, createParams
        return uiManager.instance().create_ui_new(namespace, uiname, param)
    else:
        uidefDict, param = nameSpace, uikey
        return uiManager.instance().create_ui(uidefDict, param)

def PushScreen(nameSpace, uikey, createParams=None): # type: (str, str, dict) -> any
    return uiManager.instance().push_screen(nameSpace, uikey, createParams)

def PopTopUI(): # type: () -> bool
    return uiManager.instance().pop_screen()

def GetUiScreenStack(): # type: () -> list[any]
    return uiManager.instance()._ui_screen_stack

def SetEnableGaussianBlur(enable): # type: (bool) -> bool
    return postprocess.set_enable_gaussian_blur(enable)

def CheckGaussianBlurEnabled(): # type: () -> bool
    return postprocess.check_enbale_gaussian_blur()

def SetGaussianBlurRadius(radius): # type: (float) -> bool
    return postprocess.set_gaussian_blur_radius(radius)

def GetScreenSize(): # type: () -> tuple[float, float]
    ''' 获取游戏中的屏幕大小，受ui缩放影响 '''
    return clientlevel.get_screen_size()

def GetClientScreenSize(): # type: () -> tuple[float, float]
    ''' 获取客户端屏幕大小 '''
    return gui.get_client_screen_size()

def GetInputCoord(): # type: () -> tuple[int, int]
    ''' 获取点击的实际坐标 '''
    return gui.get_input_coord()

def GetInputPos(): # type: () -> tuple[float, float]
    pos = GetInputCoord()
    if not pos:
        return
    
    screenX, screenY = GetScreenSize()
    clientX, clientY = GetClientScreenSize()

    return (pos[0] * screenX * 1.0 / clientX, pos[1] * screenY * 1.0 / clientY)

def GetMousePos(): # type: () -> tuple[float, float]
    return gui.get_mouse_position()

def GetUI(args1, args2 = None, args3 = None): # type: (str, str, dict) -> any
    uiManager = Module('client.ui.uiManager')
    if args2 is None:
        uiDef = args1
        return uiManager.instance().get_ui(uiDef)
    else:
        namespace, uiname, param = args1, args2, args3
        return uiManager.instance().get_ui_new(namespace, uiname, param)
