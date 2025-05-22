# -*- coding: utf-8 -*-

'''
ChrMod
author: Eison
version: 1.0.0
'''

from . import chrmod
import mod_log
import sys
import imp # type: ignore

def is_vanilla_loaded():
    # type: () -> bool
    return "mod.client.extraClientApi" in sys.modules

if is_vanilla_loaded():
    mod_log.logger.info("[MCP Mod Loader] -> chrmod.main()")
    chrmod.main()
else:
    pass