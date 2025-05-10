# -*- coding: utf-8 -*-

from .command.manager import CommandManager

class ChrMod(object):
    def __init__(self):
        self.command_manager = CommandManager()