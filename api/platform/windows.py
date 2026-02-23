# -*- coding: utf-8 -*-
# author Eison
# 2024/07/22

def GetWindowHandle(helperMgr): # type: (any) -> int
    return helperMgr.PyCallFunc('user32.dll', 'GetForegroundWindow')

def ByteToLPCSTR(helperMgr, str_tmp, length=1): # type: (any, str, int) -> int
    str_addr = helperMgr.PyCallFunc('ucrtbase.dll', 'malloc', len(str_tmp) + length)
    if str_addr == 0:
        return 0
    str_addr = helperMgr.PyCallFunc('ucrtbase.dll', 'memset', str_addr, 0, len(str_tmp) + length)
    helperMgr.PyCallFunc('ucrtbase.dll', 'memcpy', str_addr, id(str_tmp) + helperMgr.PyGetStringOffset(), len(str_tmp))
    return str_addr

def ByteToLPCWSTR(helperMgr, str_tmp): # type: (any, str) -> int
    wstr_tmp = str_tmp.encode('utf-16le')
    return ByteToLPCSTR(helperMgr, wstr_tmp, 2)

def SetWindowTitle(helperMgr, handle, title): # type: (any, int, str) -> bool
    return helperMgr.PyCallFunc('user32.dll', 'SetWindowTextW', handle, ByteToLPCWSTR(helperMgr, title)) == 1