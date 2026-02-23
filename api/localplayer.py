# -*- coding: utf-8 -*-
# author Eison
# 2024/07/15

from ..importer import Module

camera            = Module('camera')
_entitymodule     = Module('_entitymodule')
localplayermodule = Module('localplayermodule')
setting           = Module('setting')
player            = Module('player')

def Teleport(position): # type: (tuple[float, float, float]) -> bool
    ''' 这个和SetPosition都可以用 '''
    return camera.set_camera_pos(position)

def SetPosition(position): # type: (tuple[float, float, float]) -> None
	_entitymodule.set_player_position_and_rotation(position, (0, 0))

def GetPickRange(): # type: () -> float
    return localplayermodule.getPickRange()

def SetPickRange(range): # type: (float) -> bool
    return localplayermodule.setPickRange(range)

def PickFacing(): # type: () -> dict[str, any]
    return camera.pick_facing()

def GetCameraRotation(): # type: () -> tuple[float, float]
    return camera.get_camera_rot()

def IsSneaking(entityId): # type: (str | int) -> bool
    return localplayermodule.isSneaking(entityId)

def DepartCamera(): # type: () -> None
    camera.depart()

def UnDepartCamera(): # type: () -> None
    camera.un_depart()

def GetPerspective(): # type: () -> int
    return setting.get_player_view_perspective()

def SetPerspective(persp): # type: (int) -> bool
    return setting.set_player_view_perspective(persp)

def LockPerspective(persp): # type: (int) -> bool
    return player.set_lock_player_view_mode(persp)