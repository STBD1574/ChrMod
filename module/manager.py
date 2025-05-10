# -*- coding: utf-8 -*-

from .module import Module

class ModuleManager(object):
    def __init__(self):
        self._modules = { } # type: dict[str, Module]

    def register_module(self, module):
        # type: (Module) -> None
        self._modules[module.name] = module

    def init(self):
        pass