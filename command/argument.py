# -*- coding: utf-8 -*-

from .manager import CommandManager
from .parameter_type import ParameterType, parameter_types

class CommandArgument:
    def __init__(self, manager, args):
        self.manager = manager # type: CommandManager
        self.args = args       # type: list

    def get_argument(self, index, as_type=ParameterType.STRING):
        # type: (int, ParameterType) -> any
        """
        Get the argument at the specified index.
        """
        args_length = 1
        
        if as_type not in parameter_types:
            raise ValueError("Invalid argument type: " + str(as_type))
        
        if not self.has_argument(index, args_length):
            raise IndexError("Not enough arguments")
        
        if as_type == ParameterType.BLOCKPOS: # special case for blockpos
            args_length = 3
        
        return as_type.convert_func(self.args[index - 1:index - 1 + args_length])
    
    def has_argument(self, index, args_length=1):
        # type: (int, int) -> bool
        """
        Check if the specified argument exists.
        """

        return (index - 1 + args_length) < len(self.args)
        