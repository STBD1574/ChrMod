# -*- coding: utf-8 -*-

from .parameter_type import ParameterType, ParameterTypes

class CommandArgument(object):
    def __init__(self, args):
        self._args = args       # type: list

    def get_argument(self, index, as_type=ParameterTypes.STRING):
        # type: (int, ParameterType) -> any
        """
        Get the argument at the specified index.
        """
        args_length = 1
        
        if as_type not in ParameterTypes.__dict__.values():
            raise ValueError("Invalid argument type: " + str(as_type))
        
        if not self.has_argument(index, args_length):
            raise IndexError("Not enough arguments")
        
        if as_type == ParameterTypes.BLOCKPOS: # special case for blockpos
            args_length = 3
        
        return as_type.convert_func(self._args[index - 1:index - 1 + args_length])
    
    def has_argument(self, index, args_length=1):
        # type: (int, int) -> bool
        """
        Check if the specified argument exists.
        """

        return (index - 1 + args_length) < len(self._args)
    
    def size(self):
        # type: () -> int
        """
        Get the length of arguments.
        """
        return len(self._args)
        
    def __len__(self):
        # type: () -> int
        return self.size()