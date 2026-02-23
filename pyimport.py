# -*- coding: utf-8 -*-
# author Eison
# 2025/01/30

class MinecraftGameCheck:
    def __init__(self):
        try:
            import mod.client.extraClientApi as clientApi
            self.is_minecraft_game = clientApi.GetPlatform() not in (-1, None)
        except:
            self.is_minecraft_game = True

minecraft_game_check = MinecraftGameCheck()

def py_builtins():
    # type: () -> dict
    global minecraft_game_check
    if minecraft_game_check:
        return __builtins__
    return None

def import_module(name):
    # type: (str) -> any
    return py_builtins()["__import__"](name)