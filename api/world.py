# -*- coding: utf-8 -*-
# author Eison
# 2024/07/15

from ..importer import Module

clientlevel = Module('clientlevel')

def GetBlock(pos): # type: (tuple[int, int, int]) -> tuple[str, int]
    return clientlevel.get_block_and_data(pos)