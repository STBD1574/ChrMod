# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

class Value(object):
    __metaclass__ = ABCMeta
    
    def __init__(self, name, default_value):
        # type: (str, any) -> None
        self.name = name
        self.default_value = default_value
        self._value = default_value # type: any

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._validate(val)
        self._value = val

    def reset(self):
        self._value = self.default_value

    @abstractmethod
    def _validate(self, value):
        # type: (type) -> None
        pass

    @abstractmethod
    def serialize(self):
        # type: () -> str
        pass 

    @abstractmethod
    def deserialize(self, serialized_value):
        # type: (str) -> None
        pass


class NumericValue(Value):
    def __init__(self, name, default_value, value_range, value_type):
        super(NumericValue, self).__init__(name, default_value)
        self.value_type = value_type
        self.value_range = value_range

    def _validate(self, value):
        if not isinstance(value, self.value_type):
            raise TypeError("Expected %s, got %s" % 
                          (self.value_type.__name__, type(value).__name__))
        low, high = self.value_range
        if not (low <= value <= high):
            raise ValueError("Value out of range [%s, %s]" % (low, high))

    def serialize(self):
        return self.value_type(self.value)

    def deserialize(self, serialized_value):
        try:
            parsed = self.value_type(serialized_value)
        except (TypeError, ValueError):
            parsed = self.default_value
        self.value = parsed


class FloatValue(NumericValue):
    def __init__(self, name, default_value, value_range):
        # type: (str, float, tuple[float, float]) -> None
        super(FloatValue, self).__init__(name, default_value, value_range, float)


class IntValue(NumericValue):
    def __init__(self, name, default_value, value_range):
        # type: (str, int, tuple[int, int]) -> None
        super(IntValue, self).__init__(name, default_value, value_range, int)


class StringValue(Value):
    def _validate(self, value):
        if not isinstance(value, basestring): # type: ignore
            raise TypeError("Expected string")

    def serialize(self):
        # type: () -> str
        return unicode(self.value) # type: ignore

    def deserialize(self, serialized_value):
        # type: (str) -> None
        self.value = unicode(serialized_value) # type: ignore


class ListValue(Value):
    def __init__(self, name, default_value, valid_choices):
        super(ListValue, self).__init__(name, default_value)
        self.valid_choices = set(valid_choices)

    def _validate(self, value):
        if value not in self.valid_choices:
            raise ValueError("Invalid choice")

    def serialize(self):
        # type: () -> str
        return self.value

    def deserialize(self, serialized_value):
        # type: (str) -> None
        if serialized_value in self.valid_choices:
            self.value = serialized_value
        else:
            self.reset()
