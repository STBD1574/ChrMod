# -*- coding: utf-8 -*-

import gui           # type: ignore
import entity_module # type: ignore

class ModGameInfo(object):
    def __init__(self):
        
        self._target_player_ids = []

        self._event_handlers = []

    @property
    def local_player_id(self):
        # type: () -> str
        return entity_module.get_local_player_id()
    
    @property
    def target_player_ids(self):
        # type: () -> list
        return self._target_player_ids
    
    def display_client_message(self, message):
        # type: (str) -> None
        """
        Display a message in the left corner of the screen, for infinitely long.
        """

        while len(message) > 0:
            message = message[:600]
            gui.set_left_corner_notify_msg(message)
    