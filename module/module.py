# -*- coding: utf-8 -*-

from abc import abstractmethod
from .module_category import ModuleCategory

class Module:
    def __init__(self, name, category, enabled=True):
        # type: (str, ModuleCategory, bool) -> None
        self.name = name
        self.category = category

        self._enabled = enabled

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        if not isinstance(value, bool):
            raise TypeError("enabled must be a boolean")
        
        if value:
            self.on_enable()
        else:
            self.on_disable()

            

    @abstractmethod
    def on_enable(self):
        pass

    @abstractmethod
    def on_disable(self):
        pass