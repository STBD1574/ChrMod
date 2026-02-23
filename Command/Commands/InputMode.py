# -*- coding: utf-8 -*-
from ChrMod.Command.CommandManager import Command
import ChrMod.Api as Api
import setting


inputMode = 0

def SetInputMode(mode):
    global inputMode
    inputMode = mode

class InputMode(Command):
    def __init__(self):
        Command.__init__(self, "inputmode", "修改ModAPI识别的InputMode (1：Keyboard； 2：Touch； 3：GamePad)。", ".inputmode <inputmode>")
        original_GetToggleOption = setting.get_toggle_option
        def get_toggle_option(optionId):
            if optionId == "INPUT_MODE":
                return inputMode - 1
            return original_GetToggleOption(optionId)
        setting.get_toggle_option = get_toggle_option

    def Execute(self, label, args):
        if len(args) > 0:
            try:
                SetInputMode(int(args[0]))
                Api.Message("§cC§eh§ar§bMod §7>> §r修改成功!")
            except:
                return False
        else:
            return False
        return True