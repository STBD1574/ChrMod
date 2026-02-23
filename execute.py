# -*- coding: utf-8 -*-
import ChrMod.Api as Api
import mod.client.extraClientApi as clientApi
import traceback
import fop

def ExecutePython(script):
    try:
        exec(script)
    except:
        Api.Message('§cC§eh§ar§bMod §7>> §r运行出错! ' + traceback.format_exc())

def ExecuteFile(pyfile):
    try:
        file = open(pyfile, "r")
        ExecutePython(file.read())
        file.close()
    except:
        return False
    return True