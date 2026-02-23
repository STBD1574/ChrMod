# -*- coding: utf-8 -*-
# author Eison
# 2024/07/16

from ..api import ui

class Controls:
    SCREEN = 'common.base_screen'
    PANEL = 'common.empty_panel'
    LABEL = 'common.button_text'
    BUTTON = 'common.button'
    IMAGE = 'common.chevron_image'
    GRID = 'common.container_grid'
    SCROLL_VIEW = 'common.scroll_view_control'
    TOGGLE = 'common.toggle'
    EDIT_BOX = 'common.text_edit_box'
    STACK_PANEL = 'common.vertical_stack_panel'

def Screen(nameSpace, uiKey, clsPath): 
    return ui.RegisterUI(nameSpace, uiKey, clsPath, Controls.SCREEN)

def Panel(screenNode, uiName, parentControl=None, forceUpdate=True): #type: (any, str, any, bool) -> any
    return screenNode.CreateChildControl(Controls.PANEL, uiName, parentControl, forceUpdate)

def Label(screenNode, uiName, parentControl=None, forceUpdate=True): #type: (any, str, any, bool) -> any
    return screenNode.CreateChildControl(Controls.LABEL, uiName, parentControl, forceUpdate).asLabel()

def Button(screenNode, uiName, parentControl=None, forceUpdate=True): #type: (any, str, any, bool) -> any
    return screenNode.CreateChildControl(Controls.BUTTON, uiName, parentControl, forceUpdate).asButton()

def Image(screenNode, uiName, parentControl=None, forceUpdate=True): #type: (any, str, any, bool) -> any
    return screenNode.CreateChildControl(Controls.IMAGE, uiName, parentControl, forceUpdate).asImage()

def Grid(screenNode, uiName, parentControl=None, forceUpdate=True): #type: (any, str, any, bool) -> any
    return screenNode.CreateChildControl(Controls.GRID, uiName, parentControl, forceUpdate).asGrid()

def ScrollView(screenNode, uiName, parentControl=None, forceUpdate=True): #type: (any, str, any, bool) -> any
    return screenNode.CreateChildControl(Controls.SCROLL_VIEW, uiName, parentControl, forceUpdate).asScrollView()

def Toggle(screenNode, uiName, parentControl=None, forceUpdate=True): #type: (any, str, any, bool) -> any
    return screenNode.CreateChildControl(Controls.TOGGLE, uiName, parentControl, forceUpdate).asSwitchToggle()

def EditBox(screenNode, uiName, parentControl=None, forceUpdate=True): #type: (any, str, any, bool) -> any
    return screenNode.CreateChildControl(Controls.EDIT_BOX, uiName, parentControl, forceUpdate).asTextEditBox()

def StackPanel(screenNode, uiName, parentControl=None, forceUpdate=True): #type: (any, str, any, bool) -> any
    return screenNode.CreateChildControl(Controls.STACK_PANEL, uiName, parentControl, forceUpdate).asStackPanel()

# ==== helper functions ====

def SetFullSize(control): # type: (any) -> None
    map(lambda x : control.SetFullSize(x, {'fit': True}), {'x', 'y'})

def SetAnchor(control, anchor): # type: (any, str) -> None
    map(lambda x : x(anchor), {control.SetAnchorFrom, control.SetAnchorTo})
