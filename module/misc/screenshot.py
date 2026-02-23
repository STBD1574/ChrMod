# -*- coding: utf-8 -*-

import logging
from ..module import Module, Category
from ...module.setting import SettingEntry, ValueType
from ...pyimport import Module as fModule
from ...api import client

class PyRpcLogger(Module):
    def __init__(self):
        Module.__init__(self, "PyRpcLogger", "PyRpc数据包记录器（单向记录）。", Category.MISC, None)