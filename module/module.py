# -*- coding: utf-8 -*-
# author Eison
# 2024/07/14

from mod.common.minecraftEnum import KeyBoardType # plaese do not remove it.
from ..api.client import DisplayClientMessage
from .setting import SettingEntry, ValueType
from abc import abstractmethod

class Category:
	COMBAT = 'COMBAT'
	VISUAL = 'VISUAL'
	MOVEMENT = 'MOVEMENT'
	MISC = 'MISC'

class Module:
    def __init__(self, name, description, category, key): # type: (str, str, str, str) -> None
        self.nameToSettings = { }    # type: dict[str, SettingEntry]
        self.settings = { }          # type: dict[int, SettingEntry]
        self.settingNewIndex = 0
        self.enabled = False

        self.name = name               # type: str
        self.description = description # type: str
        self.category = category       # type: str
        self.key = key                 # type: str
        
        self.RegisterSetting(SettingEntry('KeyBind', ValueType.INT, self.key, 0, 0xFF))
        self.RegisterSetting(SettingEntry('Enabled', ValueType.BOOL, self.enabled))

    def RegisterSetting(self, settingEntry): # type: (SettingEntry) -> None
        self.nameToSettings[settingEntry.name.lower()] = settingEntry
        self.settings[self.settingNewIndex] = settingEntry
        self.settingNewIndex += 1

    def GetEnabled(self): # type: () -> bool
        return self.enabled
    
    def GetSetting(self, name): # type: (str) -> SettingEntry | None
        lowerName = name.lower()
        if lowerName in self.nameToSettings:
            return self.nameToSettings[lowerName]
        return None

    def SetEnabled(self, isEnabled): # type: (bool) -> None
        self.enabled = isEnabled
        DisplayClientMessage('§cC§eh§ar§bMod §7>§r {} {}'.format(self.name, 'Enabled ■' if isEnabled else 'Disabled □'))

        if isEnabled:
            self.OnEnable()
        else:
            self.OnDisable()

    @abstractmethod
    def OnEnable(self):
        pass

    @abstractmethod
    def OnDisable(self):
        pass

    @abstractmethod
    def OnSettingUpdate(self, settingEntry): # type: (SettingEntry) -> None
        {
            'Enabled': lambda entry : self.SetEnabled(entry.value),
            'KeyBind': lambda entry : self.__dict__.update({'key': entry.value})
        }.get(settingEntry.name, lambda _ : None)(settingEntry)
