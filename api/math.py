# -*- coding: utf-8 -*

from ..importer import Module

entity_module = Module('entity_module')

def SetPrecision(value, precision):
	return float('%.{}f'.format(precision) % value)

def Distance(pos1, pos2): #type: (tuple[float, float, float], tuple[float, float, float]) -> float
	return ((pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1]) ** 2 + (pos2[2] - pos1[2]) ** 2) ** 0.5

def GetDirectionFromRotation(rotation): #type: (tuple[float, float]) -> tuple[float, float, float]
	return entity_module.dir_from_rot(rotation)

def GetRotationFromDirection(direction): #type: (tuple[float, float, float]) -> tuple[float, float]
	return entity_module.rot_from_dir(direction)
