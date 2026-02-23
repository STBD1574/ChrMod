# -*- coding: utf-8 -*-
# author Eison
# 2025/02/08

from . import pyimport
from . import hook

game_ruler = pyimport.import_module("game_ruler") # import game_ruler
setting = pyimport.import_module("setting") # import setting

class Patch:
    """
    platform:
        0: windows
        1: ios
        2: android
        3: linux

    input_mode:
        1: keyboard and mouse
        2: touch
        3: gamepad
        4: VR
    """

    def __init__(self, platform, input_mode):
        self._platform = platform
        self._input_mode = input_mode

        self.original_is_android = hook.function_hook(game_ruler.is_android, lambda : self._platform == 2)
        self.original_is_ios = hook.function_hook(game_ruler.is_ios, lambda : self._platform == 1)
        self.original_is_windows = hook.function_hook(game_ruler.is_windows, lambda : self._platform == 0)
        self.original_is_linux = hook.function_hook(game_ruler.is_linux, lambda : self._platform == 3)


        def get_toggle_option(optionId):
            if optionId == "INPUT_MODE":
                return self._input_mode
            return self.original_get_toggle_option(optionId)
        
        self.original_get_toggle_option = hook.function_hook(setting.get_toggle_option, get_toggle_option)

    def __del__(self):
        hook.function_unhook(game_ruler.is_android, self.original_is_android)
        hook.function_unhook(game_ruler.is_ios, self.original_is_ios)
        hook.function_unhook(game_ruler.is_windows, self.original_is_windows)
        hook.function_unhook(game_ruler.is_linux, self.original_is_linux)
        hook.function_unhook(setting.get_toggle_option, self.original_get_toggle_option)

    @property
    def platform(self):
        return self._platform
    
    @platform.setter
    def platform(self, value):
        self._platform = value

    @property
    def input_mode(self):
        return self._input_mode

    @input_mode.setter
    def input_mode(self, value):
        self._input_mode = value