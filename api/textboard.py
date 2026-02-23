# -*- coding: utf-8 -*-

from ..importer import Module

sfx = Module('sfx')

def SetText(boardId, text): # type: (int, str) -> bool
    return sfx.set_text(boardId, text)

def SetBoardDepthTest(boardId, depthTest): # type: (int, bool) -> bool
    return sfx.set_depth_test(boardId, depthTest)

def SetBoardScale(boardId, scale): # type: (int, tuple[float, float]) -> bool
    if not isinstance(scale, tuple) or not len(scale) == 2:
        return False
    for v in scale:
        if not (isinstance(v, int) or isinstance(v, float)) or v <= 0:
            return False
        
    return sfx.set_scale(boardId, (scale[0], scale[1], 1.0))

def SetBoardBackgroundColor(boardId, backgroundColor): # type: (int, tuple[float, float, float, float]) -> bool
    return sfx.set_text_background_color(boardId, backgroundColor)

def SetBoardPos(boardId, pos): # type: (int, tuple[float, float, float]) -> bool
    return sfx.set_pos(boardId, pos)

def SetBoardRot(boardId, rot): # type: (int, tuple[float, float, float]) -> bool
    return sfx.set_rot(boardId, rot)

def SetBoardTextColor(boardId, textColor): # type: (int, tuple[float, float, float, float]) -> bool
    return sfx.set_text_front_color(boardId, textColor)

def SetBoardBindEntity(boardId, bindEntityId, offset, rot): # type: (int, str, tuple[float, float, float], tuple[float, float, float]) -> bool
    return sfx.bind_entity_change(boardId, bindEntityId, offset, rot)

def SetBoardFaceCamera(boardId, faceCamera): # type: (int, bool) -> bool
    return sfx.set_face_camera(boardId, faceCamera)

def CreateTextBoardInWorld(text, textColor, boardColor = None, faceCamera = True): # type: (str, tuple[float, float, float, float], tuple[float, float, float, float], bool) -> int
    suc, boardId, errMsg = sfx.create_textboard(text, textColor, boardColor, faceCamera)
    if suc:
        return boardId

def RemoveTextBoard(boardId): # type: (int) -> bool
    return sfx.remove_sfx(boardId)

def CreateSFXTextBoard(text, textColor, bindEntityId, offset, boardColor = None): # type: (str, tuple[float, float, float, float], str, tuple[float, float, float], tuple[float, float, float, float]) -> bool
    suc, boardId, errMsg = sfx.create_textboard(text, textColor, boardColor, True)
    if suc:
        return sfx.bind_entity_change(boardId, bindEntityId, offset, (0.0, 0.0, 0.0))
    return False