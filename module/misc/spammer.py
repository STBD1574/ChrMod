# -*- coding: utf-8 -*-

from ...module.module import Module, Category, KeyBoardType
from ...module.setting import SettingEntry, ValueType
from ...api import client

class Spammer(Module):
    def __init__(self):
        Module.__init__(self, 'Spammer', '自动发送消息（使用\\n换行）。', Category.MISC, KeyBoardType.KEY_PG_DOWN)

        self.timer = None
        self.text = 'ChrMod on top!'
        self.delay = 1

        self.RegisterSetting(SettingEntry('Text', ValueType.TEXT, self.text))
        self.RegisterSetting(SettingEntry('Delay', ValueType.FLOAT, self.delay, 0.1, 10))

    def OnEnable(self):
        self.timer = client.AddRepeatedTimer(self.delay, self.Spammer_Func)

    def OnDisable(self):
        client.CancelTimer(self.timer)
        self.timer = None
    
    def Spammer_Func(self):
        client.SendChatMsg(self.text)
            
    def OnSettingUpdate(self, entry): # type: (SettingEntry) -> None
        Module.OnSettingUpdate(self, entry)
        {
            'Text': lambda entry : self.__dict__.update({'text': entry.value.replace('\\n', '\n')}),
            'Delay': lambda entry : self.__dict__.update({'delay': entry.value})
        }.get(entry.name, lambda entry : None)(entry)

        if self.timer:
            self.OnDisable()
            self.OnEnable()