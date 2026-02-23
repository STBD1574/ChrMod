# -*- coding: utf-8 -*-
# author Eison
# 2024/07/16

from mod.client.ui.screenNode import ScreenNode
from ..module import manager
from ..ui import creator
from ..api import ui, client

class ClickGUI(ScreenNode):
	def __init__(self, namespace, name, param):
		ScreenNode.__init__(self, namespace, name, param)

		self.bgImg = param['background']
		self.module = param['module']

		self._scroll = None
		self._scroll_initial_pos = (0.0, 0.0)
		self._mouse_initial_pos = (0.0, 0.0)

	def Create(self):
		print(' ==== ClickGUI Create ==== ')
		ui.SetEnableGaussianBlur(True)
		parent = self.GetBaseUIControl('/variables_button_mappings_and_controls/screen_background/background')

		# Create background
		background = creator.Image(self, 'bgImage', parent, False)
		background.SetSprite(self.bgImg)
		background.SetAlpha(0.2)
		background.SetImageAdaptionType('filled')
		creator.SetFullSize(background)

		# Create close button
		closeButton = creator.Button(self, 'closeButton', parent, False)
		closeButton.AddTouchEventParams({'isSwallow': True})
		closeButton.SetSize((24, 24), True)
		closeButton.SetButtonTouchDownCallback(self.CloseButtonClick)

		image = creator.Image(self, 'image', closeButton, False)
		image.SetSprite('textures/ui/close_button_default_light.png')

		creator.SetAnchor(closeButton, 'top_right')
		creator.SetFullSize(image)

		# Create module UI 增加协程优化性能
		client.StartCoroutine(self.CreateModuleUI(parent), lambda : self.UpdateScreen(True))

	def Destroy(self):
		self.CloseButtonClick()	

	def Update(self):
		if self._scroll is None:
			return
	
		mouseX, mouseY = ui.GetMousePos()

		self._scroll.SetPosition((self._scroll_initial_pos[0] + (mouseX - self._mouse_initial_pos[0]), self._scroll_initial_pos[1] + (mouseY - self._mouse_initial_pos[1])))

	def CreateModuleUI(self, parent):
		yield
		types = manager.GetManager().GetModuleTypes()
		for i, category in enumerate(types):
			scroll = creator.StackPanel(self,  category, parent, False)
			scroll.SetOrientation('vertical')
			scroll.SetPosition((i * 64, 0))
			scroll.SetSize((64, 16), True)
	
			button = creator.Button(self, category, scroll, False)
			button.AddTouchEventParams({'isSwallow': True})
			button.SetButtonTouchDownCallback(lambda _, _scroll=scroll : self.__dict__.update({'_scroll': _scroll, '_scroll_initial_pos': _scroll.GetPosition(), '_mouse_initial_pos': ui.GetMousePos()}))
			map(lambda f : f(lambda _ : self.__dict__.update({'_scroll': None})), {button.SetButtonTouchCancelCallback, button.SetButtonTouchUpCallback})

			image = creator.Image(self, 'image', button, False)
			image.SetSprite('textures/ui/white_background.png')
			image.SetImageAdaptionType('filled')
			image.SetAlpha(0.6)
	
			creator.SetFullSize(image)
			creator.Label(self, 'text', image, False).SetText(category)
	
			for module in types[category]:
				button = creator.Button(self, module.name, scroll, False)
				button.AddHoverEventParams()
				button.AddTouchEventParams({'isSwallow': True})

				image = creator.Image(self, 'image', button, False)
				image.SetSprite('textures/ui/white_background.png')
				image.SetImageAdaptionType('filled')
				image.SetAlpha(0.5 if module.enabled else 0.4)

				button.SetButtonTouchDownCallback(lambda _, _module=module, _image=image : _module.SetEnabled((not _image.SetAlpha(0.5 if not _module.enabled else 0.4)) and (not _module.enabled)))
	
				label = creator.Label(self, 'text', image, False)
				label.SetText(module.name)
	
				creator.SetFullSize(image)

	def CloseButtonClick(self, _=None):
		ui.SetEnableGaussianBlur(False)
		ui.PopTopUI()

		self.module.enabled = False