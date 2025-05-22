# -*- coding: utf-8 -*-

class ParameterType(object):
    __slots__ = ('id', 'name', 'converter')
    
    def __init__(self, enum_id, name, converter=None):
        self.id = enum_id
        self.name = name
        self.converter = converter or (lambda x: x)

class ParameterTypes(object):
    STRING = ParameterType(0, "string", str)
    INT = ParameterType(1, "int", int)
    FLOAT = ParameterType(2, "float", float)
    BOOLEAN = ParameterType(3, "boolean", bool)
    BLOCKPOS = ParameterType(4, "blockpos", lambda args: [float(args[0]), float(args[1]), float(args[2])])
    TARGET = ParameterType(6, "target")