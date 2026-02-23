# -*- coding: utf-8 -*-
# ChrMod Gui

from mod.client.ui.screenNode import ScreenNode
from mod.client.ui.controls.baseUIControl import BaseUIControl
from mod.client.ui.controls.labelUIControl import LabelUIControl
from mod.client.ui.controls.buttonUIControl import ButtonUIControl
from mod.client.ui.controls.imageUIControl import ImageUIControl
from mod.client.ui.controls.gridUIControl import GridUIControl
from mod.client.ui.controls.scrollViewUIControl import ScrollViewUIControl
from mod.client.ui.controls.switchToggleUIControl import SwitchToggleUIControl
from mod.client.ui.controls.textEditBoxUIControl import TextEditBoxUIControl
from mod.client.ui.controls.stackPanelUIControl import StackPanelUIControl

class Controls:
    SCREEN = "common.base_screen"
    LABEL = "common.button_text"
    BUTTON = "common.button"
    IMAGE = "common.chevron_image"
    GRID = "common.container_grid"
    SCROLL_VIEW = "common.scroll_view_control"
    TOGGLE = "common.toggle"
    EDIT_BOX = "common.text_edit_box"
    STACK_PANEL = "common.vertical_stack_panel"

class ControlCreator:
    @staticmethod
    def Label(screenNode, uiName, parentControl=None, forceUpdate=True): #type: (ScreenNode, str, BaseUIControl, bool) -> LabelUIControl
        return screenNode.CreateChildControl(Controls.LABEL, uiName, parentControl, forceUpdate).asLabel()
    
    @staticmethod
    def Button(screenNode, uiName, parentControl=None, forceUpdate=True): #type: (ScreenNode, str, BaseUIControl, bool) -> ButtonUIControl
        return screenNode.CreateChildControl(Controls.BUTTON, uiName, parentControl, forceUpdate).asButton()
    
    @staticmethod
    def Image(screenNode, uiName, parentControl=None, forceUpdate=True): #type: (ScreenNode, str, BaseUIControl, bool) -> ImageUIControl
        return screenNode.CreateChildControl(Controls.IMAGE, uiName, parentControl, forceUpdate).asImage()
    
    @staticmethod
    def Grid(screenNode, uiName, parentControl=None, forceUpdate=True): #type: (ScreenNode, str, BaseUIControl, bool) -> GridUIControl
        return screenNode.CreateChildControl(Controls.GRID, uiName, parentControl, forceUpdate).asGrid()
    
    @staticmethod
    def ScrollView(screenNode, uiName, parentControl=None, forceUpdate=True): #type: (ScreenNode, str, BaseUIControl, bool) -> ScrollViewUIControl
        return screenNode.CreateChildControl(Controls.SCROLL_VIEW, uiName, parentControl, forceUpdate).asScrollView()
    
    @staticmethod
    def Toggle(screenNode, uiName, parentControl=None, forceUpdate=True): #type: (ScreenNode, str, BaseUIControl, bool) -> SwitchToggleUIControl
        return screenNode.CreateChildControl(Controls.TOGGLE, uiName, parentControl, forceUpdate).asSwitchToggle()
    
    @staticmethod
    def EditBox(screenNode, uiName, parentControl=None, forceUpdate=True): #type: (ScreenNode, str, BaseUIControl, bool) -> TextEditBoxUIControl
        return screenNode.CreateChildControl(Controls.EDIT_BOX, uiName, parentControl, forceUpdate).asTextEditBox()
    
    @staticmethod
    def StackPanel(screenNode, uiName, parentControl=None, forceUpdate=True): #type: (ScreenNode, str, BaseUIControl, bool) -> StackPanelUIControl
        return screenNode.CreateChildControl(Controls.STACK_PANEL, uiName, parentControl, forceUpdate).asStackPanel()
    
class GuiTools:
    @staticmethod
    def SetFullSize(control): #type: (BaseUIControl) -> None
        map(lambda x : control.SetFullSize(x, {"fit": True}), ["x", "y"])
