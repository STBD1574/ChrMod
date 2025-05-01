# -*- coding: utf-8 -*-

import entity_module

class ModGameInfo:
    def __init__(self):
        
        self._target_player_ids = []

    @property
    def local_player_id(self):
        # type: () -> str
        return entity_module.get_local_player_id()
    
    @property
    def target_player_ids(self):
        # type: () -> list
        return self._target_player_ids
