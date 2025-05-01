# -*- coding: utf-8 -*-

import logging

from .command.manager import CommandManager

is_running = False

def main():
    global is_running
    is_running = True
    
    CommandManager().init_commands()