# -*- coding: utf-8 -*-
# author Eison 
# 2024/04/20

from ..importer import Module

entity_module = Module('entity_module')
clientlevel   = Module('clientlevel')

def GetPosition(entityId): # type: (str | int) -> tuple[float, float, float] | None
    return entity_module.get_entity_pos(entityId)

def GetName(entityId): # type: (str | int) -> str
    return entity_module.get_player_name(entityId)

def GetType(entityId): #type: (str | int) -> str
    return entity_module.get_entity_type_str(entityId)

def GetMotion(entityId): # type: (str | int) -> tuple[float, float, float]
    return entity_module.get_actor_motion(entityId)

def IsAlive(entityId): # type: (str | int) -> bool
    return clientlevel.is_entity_alive(entityId)

def GetRotation(entityId): # type: (str | int) -> tuple[float, float]
    return entity_module.get_entity_rotation(entityId)

def SetRotation(entityId, rotation): # type: (str | int, tuple[float, float]) -> bool
    return entity_module.set_entity_rotation(entityId, rotation)

def GetBodyRotation(entityId): # type: (str | int) -> float
    return entity_module.get_entity_body_rotation(entityId)

def SetMotion(entityId, motion): # type: (str | int, tuple[float, float, float]) -> bool
    return entity_module.set_actor_motion(entityId, motion)

def IsEntityOnGround(entityId): # type: (str | int) -> bool
    return entity_module.isEntityOnGround(entityId)

def GetDistance(entityId, targetId): # type: (str | int, str | int) -> float
    ''' -1.0表示失败，好像可以提升性能 '''
    return entity_module.get_distance(entityId, targetId)

def GetEntityRider(entityId): # type: (str | int) -> int
    ''' -1 表示失败 '''
    return entity_module.get_entity_rider(entityId)