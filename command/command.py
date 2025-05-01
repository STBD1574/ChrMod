# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

from .parameter import CommandParameter # typing

class Command(metaclass=ABCMeta):
    def __init__(self, name, description, aliases):
        self._name = name               # type: str
        self._description = description # type: str
        self._aliases = aliases or []   # type: list[str]

        self._parameters = [] # type: list[CommandParameter]

    @abstractmethod
    def execute(self, args):
        # type: (list[str]) -> bool
        pass

    @property
    def name(self):
        # type: () -> str
        return self._name

    @property
    def description(self):
        # type: () -> str
        return self._description

    @property
    def aliases(self):
        # type: () -> list[str]
        return self._parameters
    
    @property
    def parameters(self):
        # type: () -> list[CommandParameter]
        return self._parameters

    def add_parameter(self, parameter):
        # type: (CommandParameter) -> None
        self.parameters.append(parameter)