# -*- coding: utf-8 -*-

from .parameter_type import ParameterType, parameter_types

class CommandParameter:
    def __init__(self, name, description, required, type, sub_parameters):
        # type: (str, str, bool, ParameterType, list[CommandParameter]) -> None
        if self.type not in parameter_types:
            raise ValueError("Invalid parameter type: " + str(self.type))

        self._name = name                     # type: str
        self._description = description       # type: str
        self._required = required             # type: bool
        self._type = type                     # type: type
        self._sub_parameters = sub_parameters # type: list[CommandParameter]

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def required(self):
        return self._required

    @property
    def type(self):
        return self._type

    @property
    def sub_parameters(self):
        return self._sub_parameters

    def __str__(self):
        # type: () -> str
        return ("<" if self.required else "[") + self.name + ': ' + str(self.type) + (">" if self.required else "]")