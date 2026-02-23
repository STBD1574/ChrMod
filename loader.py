# -*- coding: utf-8 -*-
# author Eison
# 2025/02/08

import traceback
from . import pyimport
from . import main

_log = pyimport.import_module('_log') # import _log

def _load():
    if main.is_running:
        raise Exception('Mod is already running')
    
    main.main()

def load():
    try:
        _load()
    except Exception:
        formatted = 'Error while loading mod:\n %s' % traceback.format_exc()
        with open('error.log', 'w') as f:
            _log.logError(formatted)
            f.write(formatted)