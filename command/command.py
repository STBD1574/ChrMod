# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

from .parameter import CommandParameter # typing

class Command(object, metaclass=ABCMeta):
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
        """
        Add a parameter to the command.
        """

        self.parameters.append(parameter)

    def set_variable_args(self, variable_args):
        # type: (bool) -> None
        """
        Set whether the last parameter of the command can accept variable number of arguments.
        """

        self._variable_args = variable_args