# -*- coding: utf-8 -*-

from .api import gui
from .command import command_registry
from .module import module_manager
from .event import event_listener

def main():
    command_registry.init()
    module_manager.init()
    event_listener.init()

    gui.set_left_corner_notify_msg("[DEBUG] mod loaded!")