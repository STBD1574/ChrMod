# -*- coding: utf-8 -*-

class ParameterType(tuple):
    STRING = (0, "string", str)      # type: ParameterType
    INT = (1, "int", int)            # type: ParameterType
    FLOAT = (2, "float", float)      # type: ParameterType
    BOOLEAN = (3, "boolean", bool)   # type: ParameterType
    BLOCKPOS = (4, "blockpos", lambda args: [float(args[0]), float(args[1]), float(args[2])]) # type: ParameterType
    ENUM = (5, "enum", lambda args: )                # type: ParameterType
    TARGET = (6, "target")           # type: ParameterType

    @classmethod
    def __getattr__(cls, attr):
        if attr not in cls.__dict__:
            raise AttributeError("type object " + cls.__name__ + " has no attribute " + attr)
        
        value = cls.__dict__[attr]
        if isinstance(value, tuple):
            instance = ParameterType(value)
            setattr(cls, attr, instance)
            return instance

        return value
    
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
    
parameter_types = [
    ParameterType.STRING,
    ParameterType.INT,
    ParameterType.FLOAT,
    ParameterType.BOOLEAN,
    ParameterType.ENUM,
    ParameterType.TARGET
]