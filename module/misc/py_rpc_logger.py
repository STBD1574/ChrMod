# -*- coding: utf-8 -*-

import logging
import traceback
from ..module import Module, Category
from ..setting import SettingEntry, ValueType
from ...pyimport import Module as fModule
from ...api import client

_pynetmodule = fModule('_pynetmodule')
msgpack      = fModule('msgpack')

class PyRpcLogger(Module):
    def __init__(self):
        Module.__init__(self, "PyRpcLogger", "PyRpc数据包记录器（单向记录）。", Category.MISC, None)

        self.logger = logging.getLogger('PyRpcLogger')
        self.original_send2server = None

        self.decode = True
        self.show_message = True

        self.RegisterSetting(SettingEntry('Decode', ValueType.BOOL, self.decode))
        self.RegisterSetting(SettingEntry('ShowMessage', ValueType.BOOL, self.show_message))

    def OnEnable(self):
        def net_send2server(msgId, msg, _):
            fstring = 'ModEventC2S msgId={0} msg={1}'.format(msgId, msgpack.unpackb(msg, raw=True) if self.decode else msg.encode('string_escape'))

            self.logger.info(fstring + ' ' + ''.join(traceback.format_stack()))
            client.DisplayClientMessage('§cC§eh§ar§bMod §7>§r ' + fstring)

        self.original_send2server = _pynetmodule.send2server
        _pynetmodule.send2server = net_send2server

    def OnDisable(self):
        if not self.original_send2server:
            return
        
        _pynetmodule.send2server = self.original_send2server
        self.original_send2server = None

    def OnSettingUpdate(self, settingEntry): # type: (SettingEntry) -> None
        {'Decode': lambda : self.__dict__.update({'decode': settingEntry.value}), 'ShowMessage': lambda : self.__dict__.update({'show_message': settingEntry.value})}.get(settingEntry.name, lambda : None)()
        