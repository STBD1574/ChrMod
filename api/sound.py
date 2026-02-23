# -*- coding: utf-8 -*-
# author Eison
# 2024/09/28

from ..importer import Module

audio = Module('audio')

def PlayByPlayer(name, volume, pitch): # type: (str, float, float) -> str
	""" 在player附近播放音效 """
	return audio.play_by_player(name,volume,pitch)

def PlaySound(name, pos, volume, pitch): # type: (str, tuple[float, float, float], float, float) -> str
    ''' 播放音效 '''
    return audio.play_sound(name, pos, volume, pitch)

def PlayCustomMusic(name, pos=(0,0,0), volume=1, pitch=1, loop=False, entityId = None): # type: (str, tuple[float, float, float], float, float, bool, str) -> None
    ''' 播放仅自己可见的自定义音乐 '''
    return audio.play_custom_music(name, pos, volume, pitch, loop, entityId)

def PlaySystemSound(key, pos, blockId, entityType, isBaby, isGlobal): # type: (int, tuple[float, float, float], int, int, bool, bool) -> bool
    ''' 播放系统音效，所有玩家都能听到 '''
    return audio.play_system_sound(key, pos, blockId, entityType, isBaby, isGlobal)