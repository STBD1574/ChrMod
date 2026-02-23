# -*- coding: utf-8 -*-

from ..registry import Command
from ...module import manager
from ...module.setting import ValueType
from ...api.client import DisplayClientMessage

class Setting(Command):
	def __init__(self):
		Command.__init__(self, 'setting', '模块设置命令。', '.setting <module> <setting> [value]', set())

	def Execute(self, args):
		if len(args) < 1:
			return False
		
		module = manager.GetManager().GetModule(args[0])
		if not module:
			return not DisplayClientMessage('§cC§eh§ar§bMod §7>§r 模块 {} 不存在!'.format(args[0]))

		if len(args) < 2:
			DisplayClientMessage('§b模块 {} 的设置如下：'.format(module.name))
			for index in xrange(module.settingNewIndex): # type: ignore
				setting = module.settings[index]
				DisplayClientMessage('§7{}: {} = {} [{}]'.format(setting.name, setting.valueType, setting.value, setting.defaultValue))
			return True

		setting = module.GetSetting(args[1])
		if not setting:
			return not DisplayClientMessage('§cC§eh§ar§bMod §7>§r 设置项 {} 不存在!'.format(args[1]))
		
		if len(args) < 3 and setting.valueType == ValueType.BOOL:
			setting.value = not setting.value
			return not DisplayClientMessage('§cC§eh§ar§bMod §7>§r 模块 {} 的设置 {} 已设置为 {}.'.format(module.name, setting.name, setting.value))

		value = args[2] # type: str
		try:
			if setting.valueType == ValueType.FLOAT:
				setting.value = float(value)
			elif setting.valueType == ValueType.INT:
				setting.value = int(value)
			elif setting.valueType == ValueType.BOOL:
				setting.value = value.lower() == 'true'
			elif setting.valueType == ValueType.TEXT:
				setting.value = value
			elif setting.valueType == ValueType.ENUM:
				if value.isdigit(): # get by index.
					index = int(value)
					if index >= 0 or index < setting.defaultValue.newIndex:
						entry = setting.defaultValue.GetEntry(index)
						if not entry:
							return not DisplayClientMessage('§cC§eh§ar§bMod §7>§r 请确保输入的枚举索引在范围内!')
						setting.value = entry
				else: # get by name.
					for index in xrange(setting.defaultValue.newIndex): # type: ignore
						entry = setting.defaultValue.GetEntry(index)
						if not entry:
							return not DisplayClientMessage('§cC§eh§ar§bMod §7>§r 请确保输入的枚举名称存在!')
						elif entry.lower() == value.lower():
							setting.value = entry
							break
		except ValueError:
			return not DisplayClientMessage('§cC§eh§ar§bMod §7>§r 请确保输入的设置值 {} 是一个有效的 {} 值!'.format(value, setting.valueType))

		module.OnSettingUpdate(setting)
		DisplayClientMessage('§cC§eh§ar§bMod §7>§r 模块 {} 的设置 {} 已设置为 {}.'.format(module.name, setting.name, setting.value))
		return True