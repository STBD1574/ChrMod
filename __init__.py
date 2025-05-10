# -*- coding: utf-8 -*-

'''
ChrModMod
author: Eison
version: 1.0.0
'''

from . import loader_vanilla
from . import loader_mod
import sys
import imp # type: ignore

if "mod" not in sys.modules:
    # 这里我们知道，如果vanilla.mcp已经被加载，init里就会加载mod
    loader_vanilla.load_with_vanilla()
else:
    loader_mod.load_with_mod()