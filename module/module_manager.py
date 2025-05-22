# -*- coding: utf-8 -*-

from .module import Module

class ModuleManager(object):
    _instance = None

    def __new__(cls):
        """ 
        Sigleton class. 
        """
        if not cls._instance:
            cls._instance = super(ModuleManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self._modules = { } # type: dict[str, Module]

    def register_module(self, module):
        # type: (Module) -> None
        self._modules[module.name] = module

def init():
    pass