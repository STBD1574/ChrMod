# -*- coding: utf-8 -*-

class ParameterType(tuple):
    @property
    def id(self):
        # type: () -> int
        return self[0]

    @property
    def name(self):
        # type: () -> str
        return self[1]
    
    @property
    def convert_func(self):
        # type: (callable[[str], object]) -> type
        return self[2]
    
class ParameterTypes(object):
    STRING = ParameterType(0, "string", str)
    INT = ParameterType(1, "int", int)
    FLOAT = ParameterType(2, "float", float)
    BOOLEAN = ParameterType(3, "boolean", bool)
    BLOCKPOS = ParameterType(4, "blockpos", lambda args: [float(args[0]), float(args[1]), float(args[2])]) # type: ParameterType
    ENUM = ParameterType(5, "enum")
    TARGET = ParameterType(6, "target")