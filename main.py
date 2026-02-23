# -*- coding: utf-8 -*-
# author Eison
# 2025/02/08

from . import pyimport

os = pyimport.import_module('os') # import os
game_ruler = pyimport.import_module('game_ruler') # import game_ruler

is_running = False

def make_dirs():
    file_paths = ['%schrmod/scripts', '%schrmod/logs', '%schrmod/config']

    path = './'
    if game_ruler.is_android():
        path = '/sdcard/'

    for file_path in file_paths:
        os.makedirs(file_path % path, exist_ok=True)

def main():
    '''
    ChrMod main.
    load from loader.
    '''

    global is_running
    is_running = True

    make_dirs()

    
