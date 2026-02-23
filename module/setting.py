# -*- coding: utf-8 -*-
# author Eison
# 2024/07/14

from collections import OrderedDict

class ValueType:
    FLOAT = 'FLOAT'
    INT = 'INT'
    BOOL = 'BOOL'
    TEXT = 'TEXT'
    ENUM = 'ENUM'

class SettingEnum:
	def __init__(self, *args):
		self.entries = { } # type: dict[int, str]
		self.newIndex = 0

		for arg in args:
			self.AddEntry(arg)

	def AddEntry(self, value):  # type: (str) -> None
		self.entries[self.newIndex] = value
		self.newIndex += 1

	def GetEntry(self, index):  # type: (int) -> str | None
		if index in self.entries:
			return self.entries[index]
		return None

	def SortEntries(self):  # type: () -> OrderedDict[int, str]
		return OrderedDict(sorted(self.entries.iteritems(), key=lambda item: item[0]))
	
	def __str__(self): # type: () -> str
		return ', '.join(self.entries.itervalues())

class SettingEntry:
	def __init__(self, name, valueType, defaultValue, minValue=0, maxValue=0): # type: (str, str, float | int | bool | str | SettingEnum, float | int, float | int) -> None
		self.name = name				 # type: str
		self.valueType = valueType       # type: str # if it's an ENUM, it will be seleceted ENUM index
		self.defaultValue = defaultValue # type: float | int | bool | str | SettingEnum
		self.minValue = minValue         # type: float | int
		self.maxValue = maxValue         # type: float | int

		self.value = defaultValue        # type: float | int | bool | str | SettingEnum
