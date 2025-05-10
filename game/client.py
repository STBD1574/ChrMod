# -*- coding: utf-8 -*-

import gui # type: ignore

def display_client_message(message):
    # type: (str) -> None
    """
    Display a message in the left corner of the screen, for infinitely long.
    """
    
    while len(message) > 0:
        message = message[:600]
        gui.set_left_corner_notify_msg(message)